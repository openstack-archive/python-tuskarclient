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

import logging

from openstackclient.common import utils

from tuskarclient import client as tuskar_client

LOG = logging.getLogger(__name__)

DEFAULT_MANAGEMENT_API_VERSION = '2'
API_VERSION_OPTION = 'os_management_api_version'
API_NAME = 'management'
API_VERSIONS = {
    '2': 'tuskarclient.v2.client.Client',
}


def make_client(instance):
    """Returns a management service client."""

    endpoint = instance.get_endpoint_for_service_type(
        API_NAME,
        region_name=instance._region_name,
    )

    token = instance.auth.get_token(instance.session)

    client = tuskar_client.get_client(
        instance._api_version[API_NAME],
        tuskar_url=endpoint,
        os_auth_token=token,
        username=instance._username,
        password=instance._password,
    )

    return client


def build_option_parser(parser):
    """Hook to add global options."""
    parser.add_argument(
        '--os-management-api-version',
        metavar='<management-api-version>',
        default=utils.env(
            'OS_MANAGEMENT_API_VERSION',
            default=DEFAULT_MANAGEMENT_API_VERSION),
        help='Management API version, default=' +
             DEFAULT_MANAGEMENT_API_VERSION +
             ' (Env: OS_MANAGEMENT_API_VERSION)')
    return parser
