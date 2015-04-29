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
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)


class TestDeleteManagementPlan(TestPlans):

    def setUp(self):
        super(TestDeleteManagementPlan, self).setUp()
        self.cmd = plan.DeleteManagementPlan(self.app, None)

    def test_delete_plan(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)


class TestListManagementPlan(TestPlans):

    def setUp(self):
        super(TestListManagementPlan, self).setUp()
        self.cmd = plan.ListManagementPlans(self.app, None)

    def test_list_plans(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)


class TestSetManagementPlan(TestPlans):

    def setUp(self):
        super(TestSetManagementPlan, self).setUp()
        self.cmd = plan.SetManagementPlan(self.app, None)

    def test_update_plan(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)


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
