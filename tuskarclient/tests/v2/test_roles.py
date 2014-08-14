# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock

import tuskarclient.tests.utils as tutils
from tuskarclient.v2 import roles


class RoleManagerTest(tutils.TestCase):

    def setUp(self):
        """Create a mock API object and bind to the PlanManager manager.
        """
        super(RoleManagerTest, self).setUp()
        self.api = mock.Mock()
        self.rm = roles.RoleManager(self.api)

    def test_list(self):
        """Test retrieving a list of Roles via GET."""
        self.rm._list = mock.Mock(return_value=['fake_role'])

        self.assertEqual(self.rm.list(), ['fake_role'])
        self.rm._list.assert_called_with('/v2/roles')
