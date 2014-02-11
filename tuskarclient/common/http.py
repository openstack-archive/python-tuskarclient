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

from tuskarclient import client as tuskarclient
from tuskarclient.openstack.common.apiclient import auth


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
