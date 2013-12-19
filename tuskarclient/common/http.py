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
import os
import socket

from six.moves import http_client as httplib
from six.moves.urllib import parse as urlparse
from six import StringIO

try:
    import ssl
except ImportError:
    #TODO(bcwaldon): Handle this failure more gracefully
    pass

try:
    import json
except ImportError:
    import simplejson as json

# Python 2.5 compat fix
if not hasattr(urlparse, 'parse_qsl'):
    import cgi
    urlparse.parse_qsl = cgi.parse_qsl

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
        super(HTTPClient, self).__init__(self.auth_plugin, **kwargs)

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

        if 'body' in kwargs:
            kwargs['body'] = json.dumps(kwargs['body'])

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


class VerifiedHTTPSConnection(httplib.HTTPSConnection):
    """http_client-compatibile connection using client-side SSL authentication

    :see http://code.activestate.com/recipes/
            577548-https-httplib-client-connection-with-certificate-v/
    """

    def __init__(self, host, port, key_file=None, cert_file=None,
                 ca_file=None, timeout=None, insecure=False):
        httplib.HTTPSConnection.__init__(self, host, port,
                                         key_file=key_file,
                                         cert_file=cert_file)
        self.key_file = key_file
        self.cert_file = cert_file
        if ca_file is not None:
            self.ca_file = ca_file
        else:
            self.ca_file = self.get_system_ca_file()
        self.timeout = timeout
        self.insecure = insecure

    def connect(self):
        """Connect to a host on a given (SSL) port.
        If ca_file is pointing somewhere, use it to check Server Certificate.

        Redefined/copied and extended from httplib.py:1105 (Python 2.6.x).
        This is needed to pass cert_reqs=ssl.CERT_REQUIRED as parameter to
        ssl.wrap_socket(), which forces SSL to check server certificate against
        our client certificate.
        """
        sock = socket.create_connection((self.host, self.port), self.timeout)

        if self._tunnel_host:
            self.sock = sock
            self._tunnel()

        if self.insecure is True:
            kwargs = {'cert_reqs': ssl.CERT_NONE}
        else:
            kwargs = {'cert_reqs': ssl.CERT_REQUIRED, 'ca_certs': self.ca_file}

        if self.cert_file:
            kwargs['certfile'] = self.cert_file
            if self.key_file:
                kwargs['keyfile'] = self.key_file

        self.sock = ssl.wrap_socket(sock, **kwargs)

    @staticmethod
    def get_system_ca_file():
        """Return path to system default CA file."""
        # Standard CA file locations for Debian/Ubuntu, RedHat/Fedora,
        # Suse, FreeBSD/OpenBSD
        ca_path = ['/etc/ssl/certs/ca-certificates.crt',
                   '/etc/pki/tls/certs/ca-bundle.crt',
                   '/etc/ssl/ca-bundle.pem',
                   '/etc/ssl/cert.pem']
        for ca in ca_path:
            if os.path.exists(ca):
                return ca
        return None
