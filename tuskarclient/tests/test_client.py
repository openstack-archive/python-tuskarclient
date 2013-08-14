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


class ClientGetKSClientTest(tutils.TestCase):

    @mock.patch.object(client.ksclient, 'Client')
    def test_selects_proper_values(self, mocked_ksclient):
        mocked_ksclient.return_value = 'mocked ksclient'
        kwargs = {}
        kskeys = {  # keys for KeystoneClient constructor
            'username',
            'password',
            'tenant_id',
            'tenant_name',
            'auth_url',
            'insecure',
        }
        redundant_keys = {  # key added to see if not passed to constructor
            'some_other_key',
            'any_other_key',
        }
        missing_keys = {  # keys missing to see if its value defaults to None
            'username',
            'auth_url',
        }

        # contruct testing dictionary with redunant keys and missing some
        for key in kskeys | redundant_keys:
            if key not in missing_keys:
                kwargs[key] = key + '_value'

        # construct dict containing expected values - no reduntant keys and
        # default for missing keys
        ksargs = kwargs.copy()
        for key in redundant_keys:
            del ksargs[key]

        for key in missing_keys:
            ksargs[key] = None

        self.assertEqual(client._get_ksclient(**kwargs), 'mocked ksclient')
        mocked_ksclient.assert_called_with(**ksargs)
