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

import os
import shutil
import tempfile

from tuskarclient.v2 import plans as plans_resource
from tuskarclient.v2 import roles as roles_resource
from tuskarclient.osc.v2 import plan
from tuskarclient.tests.osc.v2 import fakes


class TestPlans(fakes.TestManagement):

    def setUp(self):
        super(TestPlans, self).setUp()

        self.management_mock = self.app.client_manager.management
        self.management_mock.reset_mock()

        self.management_mock.plans.resource_class = plans_resource.Plan
        self.management_mock.roles.resource_class = roles_resource.Role

        self.management_mock.plans.list.return_value = fakes.mock_plans
        self.management_mock.roles.list.return_value = fakes.mock_roles


class TestCreateManagementPlan(TestPlans):

    def setUp(self):
        super(TestCreateManagementPlan, self).setUp()
        self.cmd = plan.CreateManagementPlan(self.app, None)

    def test_create_plan(self):
        arglist = ["Plan2", '-d', 'Plan 2']
        verifylist = [
            ('name', "Plan2"),
            ('description', "Plan 2"),
        ]

        self.management_mock.plans.create.return_value = fakes.mock_plans[1]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 2', 'Plan2', [], fakes.UUID_D)
        ], list(result)
        )

    def test_create_plan_no_description(self):
        arglist = ["Plan1", ]
        verifylist = [
            ('name', "Plan1"),
            ('description', None),
        ]

        self.management_mock.plans.create.return_value = fakes.mock_plans[0]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 1', 'Plan1', fakes.mock_roles, fakes.UUID_C)
        ], list(result))


class TestDeleteManagementPlan(TestPlans):

    def setUp(self):
        super(TestDeleteManagementPlan, self).setUp()
        self.cmd = plan.DeleteManagementPlan(self.app, None)

    def test_delete_plan(self):
        arglist = [fakes.UUID_C, ]
        verifylist = [
            ('plan', fakes.UUID_C),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.management_mock.plans.get.return_value = fakes.mock_plans[0]

        self.cmd.take_action(parsed_args)

        self.management_mock.plans.delete.assert_called_with(fakes.UUID_C)

    def test_delete_plan_by_name(self):
        arglist = ['Plan1', ]
        verifylist = [
            ('plan', 'Plan1'),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        self.management_mock.plans.delete.assert_called_with(fakes.UUID_C)


class TestListManagementPlan(TestPlans):

    def setUp(self):
        super(TestListManagementPlan, self).setUp()
        self.cmd = plan.ListManagementPlans(self.app, None)

    def test_list_plans(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        titles, rows = self.cmd.take_action(parsed_args)

        self.assertEqual(titles, ('uuid', 'name', 'description', 'roles'))
        self.assertEqual([
            (fakes.UUID_C, 'Plan1', 'Plan 1', 'Role1, Role2'),
            (fakes.UUID_D, 'Plan2', 'Plan 2', '')
        ], list(rows))


class TestSetManagementPlan(TestPlans):

    def setUp(self):
        super(TestSetManagementPlan, self).setUp()
        self.cmd = plan.SetManagementPlan(self.app, None)

    def test_update_plan_nothing(self):
        arglist = [fakes.UUID_C, ]
        verifylist = [
            ('plan', fakes.UUID_C),
            ('parameters', None),
            ('flavors', None),
            ('scales', None),
        ]

        self.management_mock.plans.get.return_value = fakes.mock_plans[1]
        self.management_mock.plans.patch.return_value = fakes.mock_plans[1]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        self.management_mock.plans.patch.assert_not_called()

    def test_update_plan_parameters(self):
        arglist = [fakes.UUID_C, '-P', 'A=1', '-P', 'B=2']
        verifylist = [
            ('plan', fakes.UUID_C),
            ('parameters', ['A=1', 'B=2']),
            ('flavors', None),
            ('scales', None),
        ]

        self.management_mock.plans.get.return_value = fakes.mock_plans[1]
        self.management_mock.plans.patch.return_value = fakes.mock_plans[1]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 2', 'Plan2', [], fakes.UUID_D)
        ], list(result))

        self.management_mock.plans.patch.assert_called_with(fakes.UUID_D, [
            {'value': '1', 'name': 'A'},
            {'value': '2', 'name': 'B'}
        ])

    def test_update_plan_parameters_by_name(self):
        arglist = ['Plan2', '-P', 'A=1', '-P', 'B=2']
        verifylist = [
            ('plan', 'Plan2'),
            ('parameters', ['A=1', 'B=2']),
            ('flavors', None),
            ('scales', None),
        ]

        self.management_mock.plans.patch.return_value = fakes.mock_plans[1]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 2', 'Plan2', [], fakes.UUID_D)
        ], list(result))

        self.management_mock.plans.patch.assert_called_with(fakes.UUID_D, [
            {'value': '1', 'name': 'A'},
            {'value': '2', 'name': 'B'}
        ])

    def test_update_plan_flavors(self):
        arglist = [fakes.UUID_C, '-F', 'Role1-1=strawberry',
                   '-F', 'Role2-2=cherry']
        verifylist = [
            ('plan', fakes.UUID_C),
            ('parameters', None),
            ('flavors', ['Role1-1=strawberry', 'Role2-2=cherry']),
            ('scales', None),
        ]

        self.management_mock.plans.get.return_value = fakes.mock_plans[0]
        self.management_mock.plans.patch.return_value = fakes.mock_plans[1]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 2', 'Plan2', [], fakes.UUID_D)
        ], list(result))

        self.management_mock.plans.patch.assert_called_with(fakes.UUID_C, [
            {'value': 'strawberry', 'name': 'Role1-1::Flavor'},
            {'value': 'cherry', 'name': 'Role2-2::Flavor'}
        ])

    def test_update_plan_scale(self):
        arglist = [fakes.UUID_C, '-S', 'Role1-1=2', '-S', 'Role2-2=3']
        verifylist = [
            ('plan', fakes.UUID_C),
            ('parameters', None),
            ('flavors', None),
            ('scales', ['Role1-1=2', 'Role2-2=3']),
        ]

        self.management_mock.plans.get.return_value = fakes.mock_plans[0]
        self.management_mock.plans.patch.return_value = fakes.mock_plans[1]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 2', 'Plan2', [], fakes.UUID_D)
        ], list(result))

        self.management_mock.plans.patch.assert_called_with(fakes.UUID_C, [
            {'value': '2', 'name': 'Role1-1::count'},
            {'value': '3', 'name': 'Role2-2::count'}
        ])


class TestShowManagementPlan(TestPlans):

    def setUp(self):
        super(TestShowManagementPlan, self).setUp()
        self.cmd = plan.ShowManagementPlan(self.app, None)

    def test_show_plan(self):
        arglist = [fakes.UUID_D, ]
        verifylist = [
            ('long', False),
        ]

        self.management_mock.plans.get.return_value = fakes.mock_plans[0]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 1', 'Plan1', 'Role1, Role2', fakes.UUID_C)
        ], list(result))

    def test_show_plan_by_name(self):
        arglist = ['Plan1', ]
        verifylist = [
            ('long', False),
        ]

        self.management_mock.plans.get.return_value = fakes.mock_plans[0]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 1', 'Plan1', 'Role1, Role2', fakes.UUID_C)
        ], list(result))

    def test_show_plan_verbose(self):
        arglist = [fakes.UUID_C, '--long']
        verifylist = [
            ('long', True),
        ]

        self.management_mock.plans.get.return_value = fakes.mock_plans[1]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 2', 'Plan2', [], fakes.UUID_D)
        ], list(result))


class TestAddManagementPlanRole(TestPlans):

    def setUp(self):
        super(TestAddManagementPlanRole, self).setUp()
        self.cmd = plan.AddManagementPlanRole(self.app, None)

    def test_add_plan_role(self):
        arglist = [fakes.UUID_C, fakes.UUID_B]
        verifylist = [
            ('plan', fakes.UUID_C),
            ('role', fakes.UUID_B),
        ]

        self.management_mock.plans.add_role.return_value = fakes.mock_plans[0]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 1', 'Plan1', fakes.mock_roles, fakes.UUID_C)
        ], list(result))

    def test_add_plan_role_by_name(self):
        arglist = ['Plan1', 'Role2']
        verifylist = [
            ('plan', 'Plan1'),
            ('role', 'Role2'),
        ]

        self.management_mock.plans.add_role.return_value = fakes.mock_plans[0]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 1', 'Plan1', fakes.mock_roles, fakes.UUID_C)
        ], list(result))

        self.management_mock.plans.add_role.assert_called_with(
            fakes.UUID_C, fakes.UUID_B)


class TestRemoveManagementPlanRole(TestPlans):

    def setUp(self):
        super(TestRemoveManagementPlanRole, self).setUp()
        self.cmd = plan.RemoveManagementPlanRole(self.app, None)

    def test_remove_plan_role(self):
        arglist = [fakes.UUID_C, fakes.UUID_B]
        verifylist = [
            ('plan', fakes.UUID_C),
            ('role', fakes.UUID_B),
        ]

        self.management_mock.plans.remove_role.return_value = (
            fakes.mock_plans[0])

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 1', 'Plan1', fakes.mock_roles, fakes.UUID_C)
        ], list(result))

    def test_remove_plan_role_by_name(self):
        arglist = ['Plan1', 'Role2']
        verifylist = [
            ('plan', 'Plan1'),
            ('role', 'Role2'),
        ]

        self.management_mock.plans.remove_role.return_value = (
            fakes.mock_plans[0])

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 1', 'Plan1', fakes.mock_roles, fakes.UUID_C)
        ], list(result))


class TestDownloadManagementPlan(TestPlans):

    def setUp(self):
        super(TestDownloadManagementPlan, self).setUp()
        self.cmd = plan.DownloadManagementPlan(self.app, None)

    def test_download_plan_templates(self):

        temp_dir = tempfile.mkdtemp()

        try:
            arglist = [fakes.UUID_C, '-O', temp_dir]
            verifylist = [
                ('plan', fakes.UUID_C),
                ('output_dir', temp_dir),
            ]

            mock_result = {
                'template-1-name': 'template 1 content',
                'template-2-name': 'template 2 content',
            }

            self.management_mock.plans.templates.return_value = mock_result

            parsed_args = self.check_parser(self.cmd, arglist, verifylist)

            self.cmd.take_action(parsed_args)

            for template_name in mock_result:
                full_path = os.path.join(temp_dir, template_name)
                self.assertTrue(os.path.exists(full_path))
        finally:
            shutil.rmtree(temp_dir)
