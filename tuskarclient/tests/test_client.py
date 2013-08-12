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

from tuskarclient.tests import utils as tutils

from tuskarclient import client

import mock


class ClientGetEndpointTest(tutils.TestCase):
    def setUp(self):
        super(ClientGetEndpointTest, self).setUp()
        self.ksclient = lambda: None
        self.ksclient.service_catalog = mock.MagicMock(name='service_catalog')
        self.ksclient.service_catalog.url_for = mock.Mock(
            return_value='http://tuskar.api:1234'
        )

    def test_default_values(self):
        return_value = client._get_endpoint(self.ksclient)
        self.assertEqual(return_value, 'http://tuskar.api:1234')
        self.ksclient.service_catalog.url_for.assert_called_with(
            service_type='management',
            endpoint_type='publicURL',
        )

    def test_kwargs_values(self):
        return_value = client._get_endpoint(
            self.ksclient,
            service_type='service_type_value',
            endpoint_type='endpoint_type_value',
            other_type='other_type_value',
        )
        self.assertEqual(return_value, 'http://tuskar.api:1234')
        self.ksclient.service_catalog.url_for.assert_called_with(
            service_type='service_type_value',
            endpoint_type='endpoint_type_value',
        )
