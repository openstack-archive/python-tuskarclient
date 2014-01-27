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

from tuskarclient.common import http
from tuskarclient.v1 import overcloud_roles
from tuskarclient.v1 import overclouds


class Client(object):
    """Client for the Tuskar v1 HTTP API.

    :param string endpoint: Endpoint URL for the tuskar service.
    :param string token: Keystone authentication token.
    :param integer timeout: Timeout for client http requests. (optional)
    """

    def __init__(self, *args, **kwargs):
        self.http_client = http.HTTPClient(*args, **kwargs)
        self.overcloud_roles = overcloud_roles.OvercloudRoleManager(
            self.http_client)
        self.overclouds = overclouds.OvercloudManager(self.http_client)
