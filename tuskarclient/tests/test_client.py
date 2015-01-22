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

import mock

from tuskarclient import client
from tuskarclient.tests import utils as tutils


class ClientGetClientTest(tutils.TestCase):
    def setUp(self):
        super(ClientGetClientTest, self).setUp()
        self.kwargs = {
            'os_username': 'os_username',
            'os_password': 'os_password',
            'os_tenant_name': 'os_tenant_name',
            'os_auth_token': 'os_auth_token',
            'os_auth_url': 'os_auth_url',
            'tuskar_url': 'tuskar_url',
        }
        self.client_kwargs = {
            'username': 'os_username',
            'password': 'os_password',
            'tenant_name': 'os_tenant_name',
            'token': 'os_auth_token',
            'auth_url': 'os_auth_url',
            'endpoint': 'tuskar_url'
        }
        self.api_version = 2

    @mock.patch.object(client, 'Client')
    def test_it_works(self, mocked_Client):
        mocked_Client.return_value = 'client'
        self.assertEqual(client.get_client(self.api_version, **self.kwargs),
                         'client')
        mocked_Client.assert_called_with(self.api_version,
                                         **self.client_kwargs)

    @mock.patch.object(client, 'Client')
    def test_it_raises_error_without_proper_params(
            self,
            mocked_Client):

        mocked_Client.return_value = None
        kwargs = self.kwargs.copy()
        del kwargs['os_password']
        self.assertRaises(ValueError,
                          client.get_client, self.api_version, **self.kwargs
                          )
        mocked_Client.assert_called_with(self.api_version,
                                         **self.client_kwargs)
