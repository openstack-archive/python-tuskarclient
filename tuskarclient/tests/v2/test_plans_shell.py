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
    for attr in ['uuid', 'name', 'description', 'attributes']:
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

    @mock.patch('tuskarclient.v2.plans_shell.print_plan_detail')
    def test_plan_create(self, mock_print_detail):
        args = empty_args()
        args.name = 'my_plan'
        args.description = 'my plan description'

        self.shell.do_plan_create(self.tuskar, args, outfile=self.outfile)
        self.tuskar.plans.create.assert_called_with(
            name='my_plan',
            description='my plan description'
        )
        mock_print_detail.assert_called_with(
            self.tuskar.plans.create.return_value, outfile=self.outfile)

    @mock.patch('tuskarclient.v2.plans_shell.print_plan_detail')
    def test_add_role(self, mock_print_detail):
        args = empty_args()
        args.plan_uuid = '42'
        args.role_uuid = 'role_uuid'

        self.shell.do_plan_add_role(self.tuskar, args, outfile=self.outfile)
        self.tuskar.plans.add_role.assert_called_with('42', 'role_uuid')

        mock_print_detail.assert_called_with(
            self.tuskar.plans.add_role.return_value, outfile=self.outfile)

    @mock.patch('tuskarclient.v2.plans_shell.print_plan_detail')
    def test_remove_role(self, mock_print_detail):
        args = empty_args()
        args.plan_uuid = '42'
        args.role_uuid = 'role_uuid'

        self.shell.do_plan_remove_role(self.tuskar, args, outfile=self.outfile)
        self.tuskar.plans.remove_role.assert_called_with('42', 'role_uuid')

        mock_print_detail.assert_called_with(
            self.tuskar.plans.remove_role.return_value, outfile=self.outfile)

    @mock.patch('tuskarclient.v2.plans_shell.print_plan_detail')
    def test_plan_patch(self, mock_print_detail):
        args = empty_args()
        args.plan_uuid = 'plan_uuid'
        args.attributes = ['foo_name=foo_value',
                           'bar_name=bar_value']
        attributes = [{'name': 'foo_name', 'value': 'foo_value'},
                      {'name': 'bar_name', 'value': 'bar_value'}]
        self.shell.do_plan_patch(self.tuskar, args, outfile=self.outfile)
        self.tuskar.plans.patch.assert_called_once()
        self.assertEqual('plan_uuid',
                         self.tuskar.plans.patch.call_args[0][0])
        self.assertEqual(
            sorted(attributes, key=lambda k: k['name']),
            sorted(self.tuskar.plans.patch.call_args[0][1],
                   key=lambda k: k['name']))

    @mock.patch('tuskarclient.v2.plans_shell.print', create=True)
    @mock.patch('tuskarclient.v2.plans_shell.os.mkdir', create=True)
    @mock.patch('tuskarclient.v2.plans_shell.os.path.isdir', create=True)
    @mock.patch('tuskarclient.v2.plans_shell.open', create=True)
    def test_plan_templates(
            self, mock_open, mock_isdir, mock_mkdir, mock_print):
        args = empty_args()
        args.plan_uuid = 'plan_uuid'
        args.output_dir = 'outdir/subdir'

        mock_isdir.return_value = False
        self.tuskar.plans.templates.return_value = {
            'name_foo': 'value_foo',
            'name_bar': 'value_bar'
        }

        self.shell.do_plan_templates(self.tuskar, args, outfile=self.outfile)

        mock_isdir.assert_called_with('outdir/subdir')
        mock_mkdir.assert_called_with('outdir/subdir')

        self.tuskar.plans.templates.assert_called_with('plan_uuid')

        mock_open.assert_any_call('outdir/subdir/name_foo', 'w+')
        mock_open.assert_any_call('outdir/subdir/name_bar', 'w+')
        self.assertEqual(mock_open.call_count, 2)

        mock_opened_file = mock_open.return_value.__enter__.return_value
        mock_opened_file.write.assert_any_call('value_foo')
        mock_opened_file.write.assert_any_call('value_bar')
        self.assertEqual(mock_opened_file.write.call_count, 2)

        mock_print.assert_any_call('Following templates has been written:')
        mock_print.assert_any_call('outdir/subdir/name_foo')
        mock_print.assert_any_call('outdir/subdir/name_bar')
        self.assertEqual(mock_print.call_count, 3)
