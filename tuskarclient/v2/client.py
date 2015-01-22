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

from tuskarclient.openstack.common.apiclient import client
from tuskarclient.v2 import plans
from tuskarclient.v2 import roles


class Client(client.BaseClient):
    """Client for the Tuskar v2 HTTP API.

    :param string endpoint: Endpoint URL for the tuskar service.
    :param string token: Keystone authentication token.
    :param integer timeout: Timeout for client http requests. (optional)
    """

    def __init__(self, http_client, extensions=None):
        super(Client, self).__init__(http_client, extensions)
        self.plans = plans.PlanManager(self)
        self.roles = roles.RoleManager(self)
