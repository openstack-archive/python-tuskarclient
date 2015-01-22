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

from tuskarclient.common import auth
from tuskarclient.common import utils
from tuskarclient.openstack.common.apiclient import client as apiclient

VERSION_MAP = {
    '2': 'tuskarclient.v2.client.Client'
}

def get_client(api_version, **kwargs):
    """Get an authtenticated client, based on the credentials
       in the keyword args.

    :param api_version: the API version to use (only '2' is valid)
    :param kwargs: keyword args containing credentials, either:
            * os_auth_token: pre-existing token to re-use
            * tuskar_url: tuskar API endpoint
            or:
            * os_username: name of user
            * os_password: user's password
            * os_auth_url: endpoint to authenticate against
            * os_tenant_{name|id}: name or ID of tenant
    """
    # Try call for client with token and endpoint.
    # If it returns None, call for client with credentials
    cli_kwargs = {
        'username': kwargs.get('os_username'),
        'password': kwargs.get('os_password'),
        'tenant_name': kwargs.get('os_tenant_name'),
        'token': kwargs.get('os_auth_token'),
        'auth_url': kwargs.get('os_auth_url'),
        'endpoint': kwargs.get('tuskar_url'),
    }
    client = Client(api_version, **cli_kwargs)
    # If we have a client, return it
    if client:
        return client
    # otherwise raise error
    else:
        raise ValueError("Need correct set of parameters")


def Client(version, **kwargs):
    client_class = apiclient.BaseClient.get_class('tuskarclient',
                                                  version,
                                                  VERSION_MAP)
    keystone_auth = auth.KeystoneAuthPlugin(
        username=kwargs.get('username'),
        password=kwargs.get('password'),
        tenant_name=kwargs.get('tenant_name'),
        token=kwargs.get('token'),
        auth_url=kwargs.get('auth_url'),
        endpoint=kwargs.get('endpoint'))
    http_client = apiclient.HTTPClient(keystone_auth)
    return client_class(http_client)
