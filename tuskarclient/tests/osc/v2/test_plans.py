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

from tuskarclient.osc.v2 import plan
from tuskarclient.tests.osc.v2 import fakes


class TestPlans(fakes.TestManagement):

    def setUp(self):
        super(TestPlans, self).setUp()

        self.management_mock = self.app.client_manager.management
        self.management_mock.reset_mock()


class TestCreateManagementPlan(TestPlans):

    def setUp(self):
        super(TestCreateManagementPlan, self).setUp()
        self.cmd = plan.CreateManagementPlan(self.app, None)

    def test_create_plan(self):
        arglist = ["Plan 2 Name", '-d', 'Plan 2']
        verifylist = [
            ('name', "Plan 2 Name"),
            ('description', "Plan 2"),
        ]

        self.management_mock.plans.create.return_value = fakes.mock_plans[1]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 2', 'Plan 2 Name', [], 'UUID2')
        ], list(result)
        )

    def test_create_plan_no_description(self):
        arglist = ["Plan1Name", ]
        verifylist = [
            ('name', "Plan1Name"),
            ('description', None),
        ]

        self.management_mock.plans.create.return_value = fakes.mock_plans[0]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 1', 'Plan 1 Name', fakes.mock_roles, 'UUID1')
        ], list(result))


class TestDeleteManagementPlan(TestPlans):

    def setUp(self):
        super(TestDeleteManagementPlan, self).setUp()
        self.cmd = plan.DeleteManagementPlan(self.app, None)

    def test_delete_plan(self):
        arglist = ['UUID1', ]
        verifylist = [
            ('plan_uuid', "UUID1"),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        self.management_mock.plans.delete.assert_called_with('UUID1')


class TestListManagementPlan(TestPlans):

    def setUp(self):
        super(TestListManagementPlan, self).setUp()
        self.cmd = plan.ListManagementPlans(self.app, None)

    def test_list_plans(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.management_mock.plans.list.return_value = fakes.mock_plans

        titles, rows = self.cmd.take_action(parsed_args)

        self.assertEqual(titles, ('uuid', 'name', 'description', 'roles'))
        self.assertEqual([
            ('UUID1', 'Plan 1 Name', 'Plan 1', 'Role 1 Name, Role 2 Name'),
            ('UUID2', 'Plan 2 Name', 'Plan 2', '')
        ], list(rows))


class TestSetManagementPlan(TestPlans):

    def setUp(self):
        super(TestSetManagementPlan, self).setUp()
        self.cmd = plan.SetManagementPlan(self.app, None)

    def test_update_plan_nothing(self):
        arglist = ['UUID1', ]
        verifylist = [
            ('plan_uuid', "UUID1"),
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
        arglist = ['UUID1', '-P', 'A=1', '-P', 'B=2']
        verifylist = [
            ('plan_uuid', "UUID1"),
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
            ('Plan 2', 'Plan 2 Name', [], 'UUID2')
        ], list(result))

        self.management_mock.plans.patch.assert_called_with('UUID1', [
            {'value': '1', 'name': 'A'},
            {'value': '2', 'name': 'B'}
        ])

    def test_update_plan_flavors(self):
        arglist = ['UUID1', '-F', 'Role 1 Name-1=strawberry',
                   '-F', 'Role 2 Name-2=cherry']
        verifylist = [
            ('plan_uuid', "UUID1"),
            ('parameters', None),
            ('flavors', ['Role 1 Name-1=strawberry', 'Role 2 Name-2=cherry']),
            ('scales', None),
        ]

        self.management_mock.plans.get.return_value = fakes.mock_plans[0]
        self.management_mock.plans.patch.return_value = fakes.mock_plans[1]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 2', 'Plan 2 Name', [], 'UUID2')
        ], list(result))

        self.management_mock.plans.patch.assert_called_with('UUID1', [
            {'value': 'strawberry', 'name': 'Role 1 Name-1::Flavor'},
            {'value': 'cherry', 'name': 'Role 2 Name-2::Flavor'}
        ])

    def test_update_plan_scale(self):
        arglist = ['UUID1', '-S', 'Role 1 Name-1=2', '-S', 'Role 2 Name-2=3']
        verifylist = [
            ('plan_uuid', "UUID1"),
            ('parameters', None),
            ('flavors', None),
            ('scales', ['Role 1 Name-1=2', 'Role 2 Name-2=3']),
        ]

        self.management_mock.plans.get.return_value = fakes.mock_plans[0]
        self.management_mock.plans.patch.return_value = fakes.mock_plans[1]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertEqual([
            ('description', 'name', 'roles', 'uuid'),
            ('Plan 2', 'Plan 2 Name', [], 'UUID2')
        ], list(result))

        self.management_mock.plans.patch.assert_called_with('UUID1', [
            {'value': '2', 'name': 'Role 1 Name-1::count'},
            {'value': '3', 'name': 'Role 2 Name-2::count'}
        ])


class TestShowManagementPlan(TestPlans):

    def setUp(self):
        super(TestShowManagementPlan, self).setUp()
        self.cmd = plan.ShowManagementPlan(self.app, None)

    def test_show_plan(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)


class TestAddManagementPlanRole(TestPlans):

    def setUp(self):
        super(TestAddManagementPlanRole, self).setUp()
        self.cmd = plan.AddManagementPlanRole(self.app, None)

    def test_add_plan_role(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)


class TestRemoveManagementPlanRole(TestPlans):

    def setUp(self):
        super(TestRemoveManagementPlanRole, self).setUp()
        self.cmd = plan.RemoveManagementPlanRole(self.app, None)

    def test_remove_plan_role(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)


class TestDownloadManagementPlan(TestPlans):

    def setUp(self):
        super(TestDownloadManagementPlan, self).setUp()
        self.cmd = plan.DownloadManagementPlan(self.app, None)

    def test_download_plan_templates(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)
