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
        keys = set([  # keys for KeystoneClient constructor
            'username',
            'password',
            'tenant_id',
            'tenant_name',
            'auth_url',
            'insecure',
        ])
        redundant_keys = set([  # key added to see if not passed to constructor
            'some_other_key',
            'any_other_key',
        ])
        missing_keys = set([  # missing to see if its val. defaults to None
            'username',
            'auth_url',
        ])

        kwargs, ksargs = tutils.create_test_dictionary_pair(keys,
                                                            redundant_keys,
                                                            missing_keys)
        self.assertEqual(client._get_ksclient(**kwargs), 'mocked ksclient')
        mocked_ksclient.assert_called_with(**ksargs)


class ClientGetClientWithTokenTest(tutils.TestCase):

    @mock.patch.object(client, 'Client')
    def test_it_filters_kwargs(self, mocked_client):
        mocked_client.return_value = 'mocked client'
        api_version = 1
        endpoint = 'http://tuskar.api:1234'
        token = 'token'

        keys = set([  # keys for Client constructor
            'insecure',
            'timeout',
            'ca_file',
            'cert_file',
            'key_file',
        ])
        redundant_keys = set([  # key added to see if not passed to constructor
            'some_other_key',
            'any_other_key',
        ])
        missing_keys = set([  # missing to see if its value defaults to None
            'ca_file',
            'cert_file',
        ])

        kwargs, client_args = tutils.create_test_dictionary_pair(
            keys, redundant_keys, missing_keys)

        self.assertEqual(client._get_client_with_token(api_version,
                                                       os_auth_token=token,
                                                       tuskar_url=endpoint,
                                                       **kwargs),
                         'mocked client')
        mocked_client.assert_called_with(api_version, endpoint,
                                         token=token,
                                         **client_args)

    def test_it_returns_none_without_token(self):
        api_version = 1
        endpoint = 'http://tuskar.api:1234'
        self.assertEqual(
            client._get_client_with_token(api_version,
                                          tuskar_url=endpoint),
            None)

    def test_it_returns_none_without_endpoint(self):
        api_version = 1
        token = 'token'
        self.assertEqual(
            client._get_client_with_token(api_version,
                                          os_auth_token=token),
            None)


class ClientGetClientWithCredentialsTest(tutils.TestCase):
    def setUp(self):
        super(ClientGetClientWithCredentialsTest, self).setUp()
        self.kwargs = {
            'os_username': 'username',
            'os_password': 'password',
            'os_tenant_id': 'tenant_id',
            'os_tenant_name': 'tenant_name',
            'os_auth_url': 'auth_url',
            'os_auth_token': 'auth_token',
            'tuskar_url': 'tuskar_url',
            'os_service_type': 'service_type',
            'os_endpoint_type': 'endpoint_type',
            'insecure': 'insecure',
        }

    def test_it_returns_none_without_username(self):
        api_version = 1
        kwargs = self.kwargs.copy()
        del kwargs['os_username']
        self.assertEqual(
            client._get_client_with_credentials(api_version, **kwargs),
            None)

    def test_it_returns_none_without_password(self):
        api_version = 1
        kwargs = self.kwargs.copy()
        del kwargs['os_password']
        self.assertEqual(
            client._get_client_with_credentials(api_version, **kwargs),
            None)

    def test_it_returns_none_without_auth_url(self):
        api_version = 1
        kwargs = self.kwargs.copy()
        del kwargs['os_auth_url']
        self.assertEqual(
            client._get_client_with_credentials(api_version, **kwargs),
            None)

    def test_it_returns_none_without_tenant_id_and_tenant_name(self):
        api_version = 1
        kwargs = self.kwargs.copy()
        del kwargs['os_tenant_id']
        del kwargs['os_tenant_name']
        self.assertEqual(
            client._get_client_with_credentials(api_version, **kwargs),
            None)

    @mock.patch.object(client, '_get_client_with_token')
    @mock.patch.object(client, '_get_token_and_endpoint')
    def test_it_calls_get_token_and_endpoint(self,
                                             mocked_get_token_and_endpoint,
                                             mocked_get_client_with_token):
        api_version = 1
        kwargs = self.kwargs.copy()
        mocked_get_token_and_endpoint.return_value = ('token', 'endpoint')
        mocked_get_client_with_token.return_value = 'mocked client'
        self.assertEqual(
            client._get_client_with_credentials(api_version, **kwargs),
            'mocked client'
        )
        mocked_get_token_and_endpoint.assert_called_with(**kwargs)
        del kwargs['tuskar_url']
        del kwargs['os_auth_token']
        mocked_get_client_with_token.assert_called_with(api_version,
                                                        os_auth_token='token',
                                                        tuskar_url='endpoint',
                                                        **kwargs)


class ClientGetTokenAndEndpointTest(tutils.TestCase):
    def setUp(self):
        super(ClientGetTokenAndEndpointTest, self).setUp()
        self.kwargs = {
            'os_username': 'username',
            'os_password': 'password',
            'os_tenant_id': 'tenant_id',
            'os_tenant_name': 'tenant_name',
            'os_auth_url': 'auth_url',
            'os_service_type': 'service_type',
            'os_endpoint_type': 'endpoint_type',
            'insecure': 'insecure',
        }
        self.translation_of_args = {
            'os_username': 'username',
            'os_password': 'password',
            'os_tenant_id': 'tenant_id',
            'os_tenant_name': 'tenant_name',
            'os_auth_url': 'auth_url',
            'os_service_type': 'service_type',
            'os_endpoint_type': 'endpoint_type',
        }
        self.redundant_keys = set(['other_key', 'any_other_key'])
        self.missing_keys = set(['os_tenant_name', 'os_service_type'])

    @mock.patch.object(client, '_get_endpoint')
    @mock.patch.object(client, '_get_ksclient')
    def test_it_with_both_token_and_endpoint(self,
                                             mocked_get_ksclient,
                                             mocked_get_endpoint):
        kwargs, expected_kwargs = tutils.create_test_dictionary_pair(
            set(self.kwargs.keys()),
            self.redundant_keys,
            self.missing_keys,
            **self.translation_of_args)

        kwargs['os_auth_token'] = 'token'
        kwargs['tuskar_url'] = 'tuskar.api:1234'

        self.assertEqual(client._get_token_and_endpoint(**kwargs),
                         ('token', 'tuskar.api:1234'))
        self.assertEqual(mocked_get_ksclient.call_count, 0)
        self.assertEqual(mocked_get_endpoint.call_count, 0)

    @mock.patch.object(client, '_get_endpoint')
    @mock.patch.object(client, '_get_ksclient')
    def test_it_with_token(self,
                           mocked_get_ksclient,
                           mocked_get_endpoint):
        kwargs, expected_kwargs = tutils.create_test_dictionary_pair(
            set(self.kwargs.keys()),
            self.redundant_keys,
            self.missing_keys,
            **self.translation_of_args)

        kwargs['os_auth_token'] = 'token'

        mocked_get_endpoint.return_value = 'tuskar.api:1234'

        self.assertEqual(client._get_token_and_endpoint(**kwargs),
                         ('token', 'tuskar.api:1234'))
        mocked_get_ksclient.assert_called_with(**expected_kwargs)
        mocked_get_endpoint.assert_called_with(
            mocked_get_ksclient.return_value,
            **expected_kwargs)
        self.assertEqual(mocked_get_ksclient.return_value.call_count, 0)

    @mock.patch.object(client, '_get_endpoint')
    @mock.patch.object(client, '_get_ksclient')
    def test_it_with_endpoint(self,
                              mocked_get_ksclient,
                              mocked_get_endpoint):
        kwargs, expected_kwargs = tutils.create_test_dictionary_pair(
            set(self.kwargs.keys()),
            self.redundant_keys,
            self.missing_keys,
            **self.translation_of_args)

        kwargs['tuskar_url'] = 'tuskar.api:1234'

        mocked_get_ksclient.return_value.auth_token = 'token'

        self.assertEqual(client._get_token_and_endpoint(**kwargs),
                         ('token', 'tuskar.api:1234'))
        mocked_get_ksclient.assert_called_with(**expected_kwargs)
        self.assertEqual(mocked_get_endpoint.call_count, 0)


class ClientGetClientTest(tutils.TestCase):
    def setUp(self):
        super(ClientGetClientTest, self).setUp()
        self.kwargs = {
            'other_key': 'other_value',
            'any_other_key': 'any_other_value',
        }
        self.api_version = 1

    @mock.patch.object(client, '_get_client_with_token')
    @mock.patch.object(client, '_get_client_with_credentials')
    def test_it_works_with_token(self,
                                 mocked_get_client_with_credentials,
                                 mocked_get_client_with_token):

        mocked_get_client_with_token.return_value = 'client'
        self.assertEqual(client.get_client(self.api_version, **self.kwargs),
                         'client')
        mocked_get_client_with_token.assert_called_with(self.api_version,
                                                        **self.kwargs)
        self.assertEqual(mocked_get_client_with_credentials.call_count, 0)

    @mock.patch.object(client, '_get_client_with_token')
    @mock.patch.object(client, '_get_client_with_credentials')
    def test_it_works_with_credentials(self,
                                       mocked_get_client_with_credentials,
                                       mocked_get_client_with_token):

        mocked_get_client_with_token.return_value = None
        mocked_get_client_with_credentials.return_value = 'client'
        self.assertEqual(client.get_client(self.api_version, **self.kwargs),
                         'client')
        mocked_get_client_with_token.assert_called_with(self.api_version,
                                                        **self.kwargs)
        mocked_get_client_with_credentials.assert_called_with(self.api_version,
                                                              **self.kwargs)

    @mock.patch.object(client, '_get_client_with_token')
    @mock.patch.object(client, '_get_client_with_credentials')
    def test_it_raises_error_without_proper_params(
            self,
            mocked_get_client_with_credentials,
            mocked_get_client_with_token):

        mocked_get_client_with_token.return_value = None
        mocked_get_client_with_credentials.return_value = None
        self.assertRaises(ValueError,
                          client.get_client, self.api_version, **self.kwargs
                          )
        mocked_get_client_with_token.assert_called_with(self.api_version,
                                                        **self.kwargs)
        mocked_get_client_with_credentials.assert_called_with(self.api_version,
                                                              **self.kwargs)


class ClientClientTest(tutils.TestCase):

    @mock.patch.object(client.utils, 'import_versioned_module')
    def test_it_works(self,
                      mocked_import_versioned_module):
        api_version = 1
        args = ['argument', 'parameter']
        kwargs = {
            'other_key': 'other_value',
            'any_other_key': 'any_other_value',
        }
        mocked_client_class = mock.MagicMock()
        mocked_import_versioned_module.return_value.Client = \
            mocked_client_class
        client.Client(api_version, *args, **kwargs)
        mocked_import_versioned_module.assert_called_with(
            api_version,
            'client'
        )
        mocked_client_class.assert_called_with(
            *args,
            **kwargs
        )
