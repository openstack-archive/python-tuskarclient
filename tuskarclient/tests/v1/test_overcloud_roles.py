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
from tuskarclient.v1 import overcloud_roles


class OvercloudRoleManagerTest(tutils.TestCase):

    def setUp(self):
        """Create a mock API object and bind to the OvercloudManager manager.
        """
        super(OvercloudRoleManagerTest, self).setUp()
        self.api = mock.Mock()
        self.rcm = overcloud_roles.OvercloudRoleManager(self.api)

    def test_get(self):
        """Test a standard GET operation to read/retrieve the Overcloud Role.
        """
        self.rcm._get = mock.Mock(return_value='fake_overcloud_role')

        self.assertEqual(self.rcm.get(42), 'fake_overcloud_role')
        self.rcm._get.assert_called_once_with('/v1/overcloud_roles/42')

    def test_get_404(self):
        """Test a 404 response to a standard GET."""
        self.rcm._get = mock.Mock(return_value=None)

        self.assertEqual(self.rcm.get('fake_overcloud_role'), None)
        self.rcm._get.assert_called_once_with(
            '/v1/overcloud_roles/fake_overcloud_role')

    def test_list(self):
        """Test retrieving a list of Overcloud Roles via GET."""
        self.rcm._list = mock.Mock(return_value=['fake_overcloud_role'])

        self.assertEqual(self.rcm.list(), ['fake_overcloud_role'])
        self.rcm._list.assert_called_once_with('/v1/overcloud_roles')

    def test_create(self):
        """Test creating a new Overcloud Role via POST."""
        self.rcm._create = mock.Mock(return_value=['fake_overcloud_role'])

        self.assertEqual(
            self.rcm.create(dummy='dummy overcloud role data'),
            ['fake_overcloud_role'])

        self.rcm._create.assert_called_once_with(
            '/v1/overcloud_roles',
            {'dummy': 'dummy overcloud role data'})

    def test_update(self):
        """Test updating a Overcloud Role via PUT."""
        self.rcm._update = mock.Mock(return_value=['fake_overcloud_role'])

        self.assertEqual(
            self.rcm.update(42, dummy='dummy overcloud role data'),
            ['fake_overcloud_role'])

        self.rcm._update.assert_called_once_with(
            '/v1/overcloud_roles/42',
            {'dummy': 'dummy overcloud role data'})

    def test_delete(self):
        """Test deleting/removing a Overcloud Role via DELETE."""
        self.rcm._delete = mock.Mock(return_value=None)

        self.assertEqual(self.rcm.delete(42), None)
        self.rcm._delete.assert_called_once_with('/v1/overcloud_roles/42')
