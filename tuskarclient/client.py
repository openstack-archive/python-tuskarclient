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

from keystoneclient.v2_0 import client as ksclient
from tuskarclient.common import utils


def _get_ksclient(**kwargs):
    """Get an endpoint and auth token from Keystone.

    :param kwargs: keyword args containing credentials:
            * username: name of user
            * password: user's password
            * auth_url: endpoint to authenticate against
            * insecure: allow insecure SSL (no cert verification)
            * tenant_{name|id}: name or ID of tenant
    """
    return ksclient.Client(username=kwargs.get('username'),
                           password=kwargs.get('password'),
                           tenant_id=kwargs.get('tenant_id'),
                           tenant_name=kwargs.get('tenant_name'),
                           auth_url=kwargs.get('auth_url'),
                           insecure=kwargs.get('insecure'))


def _get_endpoint(client, **kwargs):
    """Get an endpoint using the provided keystone client."""
    return client.service_catalog.url_for(
        service_type=kwargs.get('service_type') or 'management',
        endpoint_type=kwargs.get('endpoint_type') or 'publicURL')


def _get_token_and_endpoint(**kwargs):
    token = kwargs.get('os_auth_token')
    endpoint = kwargs.get('tuskar_url')
    ks_kwargs = {
        'username': kwargs.get('os_username'),
        'password': kwargs.get('os_password'),
        'tenant_id': kwargs.get('os_tenant_id'),
        'tenant_name': kwargs.get('os_tenant_name'),
        'auth_url': kwargs.get('os_auth_url'),
        'service_type': kwargs.get('os_service_type'),
        'endpoint_type': kwargs.get('os_endpoint_type'),
        'insecure': kwargs.get('insecure'),
    }
    # create Keystone Client if we miss token or endpoint
    if not (token and endpoint):
        _ksclient = _get_ksclient(**ks_kwargs)
        # get token if needed
        if not token:
            token = _ksclient.auth_token
        # get endpoint if needed
        if not endpoint:
            endpoint = _get_endpoint(_ksclient, **ks_kwargs)
    return token, endpoint


def _get_client_with_token(api_version, **kwargs):
    token = kwargs.get('os_auth_token')
    endpoint = kwargs.get('tuskar_url')
    # test if we have all needed parameters
    if token and endpoint:
        client_kwargs = {
            'token': token,
            'insecure': kwargs.get('insecure'),
            'timeout': kwargs.get('timeout'),
            'ca_file': kwargs.get('ca_file'),
            'cert_file': kwargs.get('cert_file'),
            'key_file': kwargs.get('key_file'),
        }
        # return new Client
        return Client(api_version, endpoint, **client_kwargs)
    # return None if we do not have all needed parameters
    else:
        return None


def _get_client_with_credentials(api_version, **kwargs):
    username = kwargs.get('os_username')
    password = kwargs.get('os_password')
    auth_url = kwargs.get('os_auth_url')
    tenant_id = kwargs.get('os_tenant_id')
    tenant_name = kwargs.get('os_tenant_name')

    # test if we have all needed parameters
    if (username and password and auth_url and
            (tenant_id or tenant_name)):
        # obtain a user token and API endpoint from keystone
        token, endpoint = _get_token_and_endpoint(**kwargs)
        kwargs['os_auth_token'] = token
        kwargs['tuskar_url'] = endpoint

        # call for a client with token and endpoint
        return _get_client_with_token(api_version, **kwargs)
    # returns None if we do not have needed parameters
    else:
        return None


def get_client(api_version, **kwargs):
    """Get an authtenticated client, based on the credentials
       in the keyword args.

    :param api_version: the API version to use ('1' or '2')
    :param kwargs: keyword args containing credentials, either:
            * os_auth_token: pre-existing token to re-use
            * tuskar_url: tuskar API endpoint
            or:
            * os_username: name of user
            * os_password: user's password
            * os_auth_url: endpoint to authenticate against
            * insecure: allow insecure SSL (no cert verification)
            * os_tenant_{name|id}: name or ID of tenant
    """
    # Try call for client with token and endpoint.
    # If it returns None, call for client with credentials
    client = (_get_client_with_token(api_version, **kwargs) or
              _get_client_with_credentials(api_version, **kwargs))
    # If we have a client, return it
    if client:
        return client
    # otherwise raise error
    else:
        raise ValueError("Need correct set of parameters")


def Client(version, *args, **kwargs):
    module = utils.import_versioned_module(version, 'client')
    client_class = getattr(module, 'Client')
    return client_class(*args, **kwargs)
