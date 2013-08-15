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

from tuskarclient import exc
from tuskarclient import shell
import tuskarclient.tests.utils as tutils


class ShellTest(tutils.TestCase):

    args_attributes = [
        'os_username', 'os_password', 'os_tenant_name', 'os_tenant_id',
        'os_auth_url', 'os_auth_token', 'tuskar_url', 'tuskar_api_version',
    ]

    def setUp(self):
        super(ShellTest, self).setUp()
        self.s = shell.TuskarShell({})

    def empty_args(self):
        args = lambda: None  # i'd use object(), but it can't have attributes
        for attr in self.args_attributes:
            setattr(args, attr, None)

        return args

    def test_ensure_auth_info_with_credentials(self):
        ensure = self.s._ensure_auth_info
        command_error = exc.CommandError
        args = self.empty_args()

        args.os_username = 'user'
        args.os_password = 'pass'
        args.os_tenant_name = 'tenant'
        self.assertRaises(command_error, ensure, args)

        args.os_auth_url = 'keystone'
        ensure(args)  # doesn't raise

    def test_ensure_auth_info_with_token(self):
        ensure = self.s._ensure_auth_info
        command_error = exc.CommandError
        args = self.empty_args()

        args.os_auth_token = 'token'
        self.assertRaises(command_error, ensure, args)

        args.tuskar_url = 'tuskar'
        ensure(args)  # doesn't raise

    def test_parser_v1(self):
        v1_commands = [
            'rack-list', 'rack-show',
        ]
        parser = self.s._parser(1)
        tuskar_help = parser.format_help()

        for arg in map(lambda a: a.replace('_', '-'), self.args_attributes):
            self.assertIn(arg, tuskar_help)

        for command in v1_commands:
            self.assertIn(command, tuskar_help)
