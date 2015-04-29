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

from tuskarclient.osc.v2 import role
from tuskarclient.tests.osc.v2 import fakes


class TestRoles(fakes.TestManagement):

    def setUp(self):
        super(TestRoles, self).setUp()

        self.management_mock = self.app.client_manager.management
        self.management_mock.reset_mock()


class TestRoleList(TestRoles):

    def setUp(self):
        super(TestRoleList, self).setUp()
        self.cmd = role.ListRoles(self.app, None)

    def test_list_roles(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.management_mock.roles.list.return_value = fakes.mock_roles

        titles, rows = self.cmd.take_action(parsed_args)

        self.assertEqual(titles, ('uuid', 'name', 'version', 'description'))
        self.assertEqual([
            ('UUID1', 'Role 1 Name', 1, 'Mock Role 1'),
            ('UUID2', 'Role 2 Name', 2, 'Mock Role 2')
        ], list(rows))
