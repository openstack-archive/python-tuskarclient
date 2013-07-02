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

import argparse
import tuskarclient.utils as utils


def create_top_parser():
    parser = argparse.ArgumentParser(prog='tuskar',
                                     description='OpenStack Management CLI',
                                     add_help=False
                                     )

    parser.add_argument('-h', '--help',
                        action='store_true',
                        help="Print this help message and exit.",
                        )

    parser.add_argument('--os-username',
                        default=utils.env('OS_USERNAME'),
                        help='Defaults to env[OS_USERNAME]',
                        )

    parser.add_argument('--os_username',
                        help=argparse.SUPPRESS,
                        )

    parser.add_argument('--os-password',
                        default=utils.env('OS_PASSWORD'),
                        help='Defaults to env[OS_PASSWORD]',
                        )

    parser.add_argument('--os_password',
                        help=argparse.SUPPRESS,
                        )

    parser.add_argument('--os-tenant-id',
                        default=utils.env('OS_TENANT_ID'),
                        help='Defaults to env[OS_TENANT_ID]',
                        )

    parser.add_argument('--os_tenant_id',
                        help=argparse.SUPPRESS,
                        )

    parser.add_argument('--os-tenant-name',
                        default=utils.env('OS_TENANT_NAME'),
                        help='Defaults to env[OS_TENANT_NAME]',
                        )

    parser.add_argument('--os_tenant_name',
                        help=argparse.SUPPRESS,
                        )

    parser.add_argument('--os-auth-url',
                        default=utils.env('OS_AUTH_URL'),
                        help='Defaults to env[OS_AUTH_URL]',
                        )

    parser.add_argument('--os_auth_url',
                        help=argparse.SUPPRESS,
                        )

    return parser
