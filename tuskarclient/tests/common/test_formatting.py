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

import tuskarclient.common.formatting as fmt
import tuskarclient.tests.utils as tutils
from tuskarclient.v2 import plans


class FormattersTest(tutils.TestCase):

    def test_attributes_formatter(self):
        """Test the attributes formatter displays the attributes correctly."""

        attributes = {
            'password': 'pass',
            'mysql_host': 'http://somewhere',
            'a thing': 'a value'
        }
        self.assertEqual(
            ("a thing=a value\nmysql_host=http://somewhere\npassword=pass\n"),
            fmt.attributes_formatter(attributes),
        )

    def test_list_plan_roles_formatter(self):
        roles = plans.Plan(None,
                           {'roles': [{'name': 'foo_role'},
                                      {'name': 'bar_role'}]}).roles
        self.assertEqual(
            "foo_role, bar_role",
            fmt.list_plan_roles_formatter(roles)
        )
