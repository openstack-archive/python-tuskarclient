# Copyright 2012 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from six import StringIO

try:
    import json
except ImportError:
    import simplejson as json

from tuskarclient import client as tuskarclient
from tuskarclient import exc as tuskar_exc
from tuskarclient.openstack.common.apiclient import auth
from tuskarclient.openstack.common.apiclient import client


LOG = logging.getLogger(__name__)
USER_AGENT = 'python-tuskarclient'
CHUNKSIZE = 1024 * 64  # 64kB


class TuskarAuthPlugin(auth.BaseAuthPlugin):

    def _do_authenticate(self, http_client):
        self.ksclient = tuskarclient._get_ksclient(**http_client.kwargs)

    def token_and_endpoint(self, endpoint_type, service_type):
        token = self.ksclient.auth_token
        endpoint = tuskarclient._get_endpoint(self.ksclient,
                                              endpoint_type=endpoint_type,
                                              service_type=service_type)
        return token, endpoint


class HTTPClient(client.HTTPClient):

    def __init__(self, endpoint, **kwargs):
        self.kwargs = kwargs
        self.endpoint = endpoint
        self.auth_plugin = TuskarAuthPlugin()
        verify = not kwargs.get('insecure', False)
        cert = kwargs.get('ca_file')
        timeout = kwargs.get('timeout')
        super(HTTPClient, self).__init__(self.auth_plugin, verify=verify,
                                         cert=cert, timeout=timeout)

    def _http_request(self, url, method, **kwargs):
        """Send an http request with the specified characteristics."""
        url = client.HTTPClient.concat_url(self.endpoint, url)
        resp = self.request(method, url, **kwargs)
        self._http_log_resp(resp)
        if resp.status_code == 300:
            # TODO(viktors): we should use exception for status 300 from common
            #                code, when we will have required exception in Oslo
            #                See patch https://review.openstack.org/#/c/63111/
            raise tuskar_exc.from_response(resp)

        body_iter = resp.iter_content(CHUNKSIZE)

        # Read body into string if it isn't obviously image data
        if resp.headers.get('content-type') != 'application/octet-stream':
            body_str = ''.join([chunk for chunk in body_iter])
            body_iter = StringIO(body_str)

        return resp, body_iter

    def json_request(self, method, url, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Content-Type', 'application/json')
        kwargs['headers'].setdefault('Accept', 'application/json')

        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])

        resp, body_iter = self._http_request(url, method, **kwargs)
        content_type = resp.headers.get('content-type')

        if resp.status_code in (204, 205) or content_type is None:
            return resp, list()

        if 'application/json' in content_type:
            body = ''.join([chunk for chunk in body_iter])
            try:
                body = json.loads(body)
            except ValueError:
                LOG.error('Could not decode response body as JSON')
        else:
            body = None

        return resp, body

    def raw_request(self, method, url, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Content-Type',
                                     'application/octet-stream')
        return self._http_request(url, method, **kwargs)
