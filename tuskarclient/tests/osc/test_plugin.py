#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import unittest

import mock

from tuskarclient.osc import plugin


class TestManagementPlugin(unittest.TestCase):

    @mock.patch("tuskarclient.client.get_client")
    def test_make_client(self, mock_get_client):

        mock_instance = mock.Mock()
        mock_instance._api_version = {'management': 2}
        mock_instance.get_endpoint_for_service_type.return_value = "ENDPOINT"
        mock_instance.auth.get_token.return_value = "TOKEN"

        plugin.make_client(mock_instance)

        mock_instance.get_endpoint_for_service_type.assert_called_with(
            'management', region_name=mock_instance._region_name)
        mock_instance.auth.get_token.assert_called_with(mock_instance.session)

        mock_get_client.assert_called_with(
            2,
            username=mock_instance._username,
            password=mock_instance._password,
            tuskar_url="ENDPOINT",
            os_auth_token="TOKEN"
        )
