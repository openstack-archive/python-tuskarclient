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
import six

import tuskarclient.tests.utils as tutils
from tuskarclient.v2 import plans_shell


def empty_args():
    args = mock.Mock(spec=[])
    for attr in ['uuid', 'name', 'description', 'capacities', 'slots',
                 'resource_class']:
        setattr(args, attr, None)
    return args


def mock_plan():
    plan = mock.Mock()
    plan.uuid = '5'
    plan.name = 'My Plan'
    return plan


class BasePlansShellTest(tutils.TestCase):

    def setUp(self):
        super(BasePlansShellTest, self).setUp()
        self.outfile = six.StringIO()
        self.tuskar = mock.MagicMock()
        self.shell = plans_shell


class PlansShellTest(BasePlansShellTest):

    @mock.patch('tuskarclient.common.formatting.print_list')
    def test_plan_list(self, mock_print_list):
        args = empty_args()

        self.shell.do_plan_list(self.tuskar, args, outfile=self.outfile)
        # testing the other arguments would be just copy-paste
        mock_print_list.assert_called_with(
            self.tuskar.plans.list.return_value, mock.ANY, mock.ANY,
            outfile=self.outfile
        )

    @mock.patch('tuskarclient.common.utils.find_resource')
    @mock.patch('tuskarclient.v2.plans_shell.print_plan_detail')
    def test_plan_show(self, mock_print_detail, mock_find_resource):
        mock_find_resource.return_value = mock_plan()
        args = empty_args()
        args.plan = '5'

        self.shell.do_plan_show(self.tuskar, args, outfile=self.outfile)
        mock_find_resource.assert_called_with(self.tuskar.plans, '5')
        mock_print_detail.assert_called_with(mock_find_resource.return_value,
                                             outfile=self.outfile)

    @mock.patch('tuskarclient.common.utils.find_resource')
    def test_plan_delete(self, mock_find_resource):
        mock_find_resource.return_value = mock_plan()
        args = empty_args()
        args.plan = '5'

        self.shell.do_plan_delete(self.tuskar, args, outfile=self.outfile)
        self.tuskar.plans.delete.assert_called_with('5')
        self.assertEqual('Deleted Plan "My Plan".\n',
                         self.outfile.getvalue())
