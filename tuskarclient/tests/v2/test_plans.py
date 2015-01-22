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
from tuskarclient.v2 import plans
from tuskarclient.v2 import roles


class PlanManagerTest(tutils.TestCase):

    def setUp(self):
        """Create a mock API object and bind to the PlanManager manager.
        """
        super(PlanManagerTest, self).setUp()
        self.api = mock.Mock()
        self.pm = plans.PlanManager(self.api)

    def test_get(self):
        """Test a standard GET operation to read/retrieve the plan."""
        self.pm._get = mock.Mock(return_value='fake_plan')

        self.assertEqual(self.pm.get('fake_plan'), 'fake_plan')
        self.pm._get.assert_called_with('/v2/plans/fake_plan')

    def test_get_404(self):
        """Test a 404 response to a standard GET."""
        self.pm._get = mock.Mock(return_value=None)

        self.assertEqual(self.pm.get('fake_plan'), None)
        self.pm._get.assert_called_with('/v2/plans/fake_plan')

    def test_list(self):
        """Test retrieving a list of plans via GET."""
        self.pm._list = mock.Mock(return_value=['fake_plan'])

        self.assertEqual(self.pm.list(), ['fake_plan'])
        self.pm._list.assert_called_with('/v2/plans')

    def test_create(self):
        """Test creating a new plan via POST."""
        self.pm._create = mock.Mock(return_value=['fake_plan'])

        self.assertEqual(
            self.pm.create(dummy='dummy plan data'),
            ['fake_plan'])

        self.pm._create.assert_called_with(
            '/v2/plans',
            {'dummy': 'dummy plan data'})

    def test_patch(self):
        """Test patching a plan."""
        self.pm._patch = mock.Mock(return_value=['fake_plan'])

        self.assertEqual(
            self.pm.patch('42', [{'name': 'dummy',
                                  'value': 'dummy plan data'}]),
            ['fake_plan'])

        self.pm._patch.assert_called_with(
            '/v2/plans/42',
            [{'name': 'dummy',
              'value': 'dummy plan data'}])

    def test_delete(self):
        """Test deleting/removing an plan via DELETE."""
        self.pm._delete = mock.Mock(return_value=None)

        self.assertEqual(self.pm.delete(42), None)
        self.pm._delete.assert_called_with('/v2/plans/42')

    def test_roles_path_with_role_id(self):
        """Test for building path for Role using UUID."""
        self.assertEqual(self.pm._roles_path('plan_42', 'role_abc'),
                         '/v2/plans/plan_42/roles/role_abc')

    def test_roles_path_without_role_id(self):
        """Test for building path for Role for POST requests."""
        self.assertEqual(self.pm._roles_path('plan_42'),
                         '/v2/plans/plan_42/roles')

    def test_add_role(self):
        """Test assigning Role to a Plan."""
        self.pm._create = mock.Mock(return_value='dummy plan')

        self.assertEqual(self.pm.add_role('42', role_uuid='qwert12345'),
                         'dummy plan')
        self.pm._create.assert_called_with(
            '/v2/plans/42/roles',
            {'uuid': 'qwert12345'})

    def test_remove_role(self):
        """Test assigning Role to a Plan."""
        self.api.delete = mock.Mock(return_value=(
            'resp',
            'fake_plan_data'))
        self.pm.resource_class = mock.Mock(return_value='fake_plan')

        self.assertEqual(self.pm.remove_role('42', role_uuid='qwert12345'),
                         'fake_plan')
        self.api.delete.assert_called_with('/v2/plans/42/roles/qwert12345')
        self.pm.resource_class.assert_called_with(self.pm, 'fake_plan_data')

    def test_templates_path(self):
        self.assertEqual(self.pm._templates_path('42'),
                         '/v2/plans/42/templates')

    def test_templates(self):
        """Test a GET operation to retrieve the plan's templates."""
        self.pm._get = mock.MagicMock()
        self.pm._get.return_value.to_dict.return_value = 'fake_templates_dict'

        self.assertEqual(self.pm.templates('fake_plan'), 'fake_templates_dict')
        self.pm._get.assert_called_with('/v2/plans/fake_plan/templates',
                                        obj_class=plans.Templates)

    def test_roles_subresource(self):
        self.pm._get = mock.Mock(
            return_value=plans.Plan(None,
                                    {'roles': [
                                        {'name': 'foo_role'},
                                        {'name': 'bar_role'}
                                    ]}))
        test_roles = self.pm.get('42').roles
        self.assertTrue(isinstance(test_roles, list))
        self.assertTrue(isinstance(test_roles[0], roles.Role))
