# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock

from tuskarclient.common import auth
from tuskarclient.openstack.common.apiclient import client
from tuskarclient.tests import utils as test_utils


@mock.patch.object(auth.ksclient, 'Client')
class KeystoneAuthPluginTest(test_utils.TestCase):
    def setUp(self):
        super(KeystoneAuthPluginTest, self).setUp()
        plugin = auth.KeystoneAuthPlugin(
            username="fake-username",
            password="fake-password",
            tenant_id="fake-tenant-id",
            tenant_name="fake-tenant-name",
            auth_url="http://auth",
            endpoint="http://tuskar")
        self.cs = client.HTTPClient(auth_plugin=plugin)

    def test_authenticate(self, mock_ksclient):
        self.cs.authenticate()
        mock_ksclient.assert_called_with(
            username="fake-username",
            password="fake-password",
            tenant_id="fake-tenant-id",
            tenant_name="fake-tenant-name",
            auth_url="http://auth")

    def test_token_and_endpoint(self, mock_ksclient):
        self.cs.authenticate()
        (token, endpoint) = self.cs.auth_plugin.token_and_endpoint(
            "fake-endpoint-type", "fake-service-type")
        self.assertIsInstance(token, mock.MagicMock)
        self.assertEqual("http://tuskar", endpoint)

    def test_token_and_endpoint_before_auth(self, mock_ksclient):
        (token, endpoint) = self.cs.auth_plugin.token_and_endpoint(
            "fake-endpoint-type", "fake-service-type")
        self.assertIsNone(token, None)
        self.assertIsNone(endpoint, None)


@mock.patch.object(auth.ksclient, 'Client')
class KeystoneAuthPluginTokenTest(test_utils.TestCase):
    def test_token_and_endpoint(self, mock_ksclient):
        plugin = auth.KeystoneAuthPlugin(
            token="fake-token",
            endpoint="http://tuskar")
        cs = client.HTTPClient(auth_plugin=plugin)

        cs.authenticate()
        (token, endpoint) = cs.auth_plugin.token_and_endpoint(
            "fake-endpoint-type", "fake-service-type")
        self.assertEqual('fake-token', token)
        self.assertEqual('http://tuskar', endpoint)
