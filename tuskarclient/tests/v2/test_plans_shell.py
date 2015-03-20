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
    for attr in ['uuid', 'name', 'description', 'parameters']:
        setattr(args, attr, None)
    return args


def mock_plan():
    plan = mock.Mock()
    plan.uuid = '5'
    plan.name = 'My Plan'
    plan.parameters = []
    plan.parameters.append({'name': 'compute-1::count', 'value': '2'})
    plan.parameters.append({'name': 'compute-1::Flavor', 'value': 'baremetal'})
    plan.to_dict.return_value = {
        'uuid': 5,
        'name': 'My Plan',
        'parameters': plan.parameters,
    }
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
    @mock.patch('tuskarclient.v2.plans_shell.print_plan_summary')
    def test_plan_show(self, mock_print_summary, mock_find_resource):
        mock_find_resource.return_value = mock_plan()
        args = empty_args()
        args.plan = '5'
        args.verbose = False

        self.shell.do_plan_show(self.tuskar, args, outfile=self.outfile)
        mock_find_resource.assert_called_with(self.tuskar.plans, '5')
        mock_print_summary.assert_called_with(mock_find_resource.return_value,
                                              outfile=self.outfile)

    @mock.patch('tuskarclient.common.utils.find_resource')
    @mock.patch('tuskarclient.common.formatting.print_dict')
    def test_plan_show_scale(self, mock_print_dict, mock_find_resource):
        mock_find_resource.return_value = mock_plan()
        args = empty_args()
        args.plan = '5'

        self.shell.do_plan_show_scale(self.tuskar, args, outfile=self.outfile)
        mock_find_resource.assert_called_with(self.tuskar.plans, '5')
        mock_print_dict.assert_called_with({'compute-1': '2'},
                                           outfile=self.outfile)

    @mock.patch('tuskarclient.common.utils.find_resource')
    @mock.patch('tuskarclient.common.formatting.print_dict')
    def test_plan_show_flavors(self, mock_print_dict, mock_find_resource):
        mock_find_resource.return_value = mock_plan()
        args = empty_args()
        args.plan = '5'

        self.shell.do_plan_show_flavors(self.tuskar, args,
                                        outfile=self.outfile)
        mock_find_resource.assert_called_with(self.tuskar.plans, '5')
        mock_print_dict.assert_called_with({'compute-1': 'baremetal'},
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

    @mock.patch('tuskarclient.v2.plans_shell.print_plan_summary')
    def test_plan_create(self, mock_print_summary):
        args = empty_args()
        args.name = 'my_plan'
        args.description = 'my plan description'

        self.shell.do_plan_create(self.tuskar, args, outfile=self.outfile)
        self.tuskar.plans.create.assert_called_with(
            name='my_plan',
            description='my plan description'
        )
        mock_print_summary.assert_called_with(
            self.tuskar.plans.create.return_value, outfile=self.outfile)

    @mock.patch('tuskarclient.v2.plans_shell.print_plan_summary')
    def test_add_role(self, mock_print_summary):
        args = empty_args()
        args.plan_uuid = '42'
        args.role_uuid = 'role_uuid'

        self.shell.do_plan_add_role(self.tuskar, args, outfile=self.outfile)
        self.tuskar.plans.add_role.assert_called_with('42', 'role_uuid')

        mock_print_summary.assert_called_with(
            self.tuskar.plans.add_role.return_value, outfile=self.outfile)

    @mock.patch('tuskarclient.v2.plans_shell.print_plan_summary')
    def test_remove_role(self, mock_print_summary):
        args = empty_args()
        args.plan_uuid = '42'
        args.role_uuid = 'role_uuid'

        self.shell.do_plan_remove_role(self.tuskar, args, outfile=self.outfile)
        self.tuskar.plans.remove_role.assert_called_with('42', 'role_uuid')

        mock_print_summary.assert_called_with(
            self.tuskar.plans.remove_role.return_value, outfile=self.outfile)

    @mock.patch('tuskarclient.common.utils.find_resource')
    def test_plan_scale(self, mock_find_resource):
        mock_find_resource.return_value = mock_plan()
        role = mock.Mock()
        role.name = 'compute'
        role.version = 1
        self.tuskar.roles.list.return_value = [role]

        args = empty_args()
        args.plan_uuid = 'plan_uuid'
        args.role_name = 'compute-1'
        args.count = '9'

        parameters = [{'name': 'compute-1::count', 'value': '9'}]

        self.shell.do_plan_scale(self.tuskar, args, outfile=self.outfile)
        self.tuskar.plans.patch.assert_called_once()
        self.assertEqual('plan_uuid', self.tuskar.plans.patch.call_args[0][0])
        self.assertEqual(
            sorted(parameters, key=lambda k: k['name']),
            sorted(self.tuskar.plans.patch.call_args[0][1],
                   key=lambda k: k['name']))

    @mock.patch('tuskarclient.common.utils.find_resource')
    def test_plan_flavor(self, mock_find_resource):
        mock_find_resource.return_value = mock_plan()
        role = mock.Mock()
        role.name = 'compute'
        role.version = 1
        self.tuskar.roles.list.return_value = [role]

        args = empty_args()
        args.plan_uuid = 'plan_uuid'
        args.role_name = 'compute-1'
        args.flavor = 'baremetalssd'

        parameters = [{'name': 'compute-1::Flavor', 'value': 'baremetalssd'}]

        self.shell.do_plan_flavor(self.tuskar, args, outfile=self.outfile)
        self.tuskar.plans.patch.assert_called_once()
        self.assertEqual('plan_uuid', self.tuskar.plans.patch.call_args[0][0])
        self.assertEqual(
            sorted(parameters, key=lambda k: k['name']),
            sorted(self.tuskar.plans.patch.call_args[0][1],
                   key=lambda k: k['name']))

    @mock.patch('tuskarclient.v2.plans_shell.print_plan_summary')
    def test_plan_patch(self, mock_print_summary):
        args = empty_args()
        args.plan_uuid = 'plan_uuid'
        args.parameters = ['foo_name=foo_value',
                           'bar_name=bar_value']
        args.attributes = None
        parameters = [{'name': 'foo_name', 'value': 'foo_value'},
                      {'name': 'bar_name', 'value': 'bar_value'}]
        self.shell.do_plan_patch(self.tuskar, args, outfile=self.outfile)
        self.tuskar.plans.patch.assert_called_once()
        self.assertEqual('plan_uuid',
                         self.tuskar.plans.patch.call_args[0][0])
        self.assertEqual(
            sorted(parameters, key=lambda k: k['name']),
            sorted(self.tuskar.plans.patch.call_args[0][1],
                   key=lambda k: k['name']))

    @mock.patch('tuskarclient.v2.plans_shell.print_plan_summary')
    def test_plan_patch_deprecated(self, mock_print_summary):
        """Test plan_patch with the deprecated --attribute flag."""
        args = empty_args()
        args.plan_uuid = 'plan_uuid'
        args.attributes = ['foo_name=foo_value',
                           'bar_name=bar_value']
        args.parameters = None
        parameters = [{'name': 'foo_name', 'value': 'foo_value'},
                      {'name': 'bar_name', 'value': 'bar_value'}]
        self.shell.do_plan_patch(self.tuskar, args, outfile=self.outfile)
        self.tuskar.plans.patch.assert_called_once()
        self.assertEqual('plan_uuid',
                         self.tuskar.plans.patch.call_args[0][0])
        self.assertEqual(
            sorted(parameters, key=lambda k: k['name']),
            sorted(self.tuskar.plans.patch.call_args[0][1],
                   key=lambda k: k['name']))

    @mock.patch('tuskarclient.v2.plans_shell.print_plan_detail')
    def test_plan_update(self, mock_print_detail):
        args = empty_args()
        args.plan_uuid = 'plan_uuid'
        args.parameters = ['foo_name=foo_value',
                           'bar_name=bar_value']
        parameters = [{'name': 'foo_name', 'value': 'foo_value'},
                      {'name': 'bar_name', 'value': 'bar_value'}]
        args.attributes = None
        self.shell.do_plan_update(self.tuskar, args, outfile=self.outfile)
        self.tuskar.plans.patch.assert_called_once()
        self.assertEqual('plan_uuid',
                         self.tuskar.plans.patch.call_args[0][0])
        self.assertEqual(
            sorted(parameters, key=lambda k: k['name']),
            sorted(self.tuskar.plans.patch.call_args[0][1],
                   key=lambda k: k['name']))

    @mock.patch('tuskarclient.common.utils.find_resource')
    def test_print_plan_summary(self, mock_find_resource):
        mock_find_resource.return_value = mock_plan()
        args = empty_args()
        args.plan = '5'
        args.verbose = False

        self.shell.do_plan_show(self.tuskar, args, outfile=self.outfile)
        mock_find_resource.assert_called_with(self.tuskar.plans, '5')

    @mock.patch('tuskarclient.common.utils.find_resource')
    def test_print_plan_detail(self, mock_find_resource):
        mock_find_resource.return_value = mock_plan()
        args = empty_args()
        args.plan = '5'
        args.verbose = True

        self.shell.do_plan_show(self.tuskar, args, outfile=self.outfile)
        mock_find_resource.assert_called_with(self.tuskar.plans, '5')

    def test_filter_parameters_to_dict(self):
        parameters = [{'name': 'compute-1::count', 'value': '2'}]
        self.assertEqual(
            self.shell.filter_parameters_to_dict(parameters, 'count'),
            {'compute-1': '2'}
        )

    @mock.patch('tuskarclient.v2.plans_shell.print', create=True)
    @mock.patch('tuskarclient.v2.plans_shell.os.mkdir', create=True)
    @mock.patch('tuskarclient.v2.plans_shell.os.path.isdir', create=True)
    @mock.patch('tuskarclient.v2.plans_shell.open', create=True)
    @mock.patch('tuskarclient.v2.plans_shell.os.path.exists', create=True)
    @mock.patch('tuskarclient.v2.plans_shell.os.makedirs', create=True)
    def test_plan_templates(
            self, mock_makedirs, mock_exists, mock_open, mock_isdir,
            mock_mkdir, mock_print):
        args = empty_args()
        args.plan_uuid = 'plan_uuid'
        args.output_dir = 'outdir/subdir'

        # Simulate the first exists check being false and the subsequent check
        # being true so as to exercise that makesdirs is only called once
        # per nested directory.
        exists_return_values = [False, True]

        def toggle_exists_result(*e_args, **e_kwargs):
            return exists_return_values.pop(0)
        mock_exists.side_effect = toggle_exists_result

        mock_isdir.return_value = False
        self.tuskar.plans.templates.return_value = {
            'name_foo': 'value_foo',
            'name_bar': 'value_bar',
            'nested/name_baz': 'value_baz',
            'nested/name_zom': 'value_zom'
        }

        self.shell.do_plan_templates(self.tuskar, args, outfile=self.outfile)

        # Initial check and creation of the output directory
        mock_isdir.assert_any_call('outdir/subdir')
        mock_mkdir.assert_any_call('outdir/subdir')

        # Checks and creation of nested directory
        self.assertEqual(mock_exists.call_count, 2)
        self.assertEqual(mock_makedirs.call_count, 1)
        mock_makedirs.assert_called_with('outdir/subdir/nested')

        self.tuskar.plans.templates.assert_called_with('plan_uuid')

        mock_open.assert_any_call('outdir/subdir/name_foo', 'w+')
        mock_open.assert_any_call('outdir/subdir/name_bar', 'w+')
        mock_open.assert_any_call('outdir/subdir/nested/name_baz', 'w+')
        mock_open.assert_any_call('outdir/subdir/nested/name_zom', 'w+')
        self.assertEqual(mock_open.call_count, 4)

        mock_opened_file = mock_open.return_value.__enter__.return_value
        mock_opened_file.write.assert_any_call('value_foo')
        mock_opened_file.write.assert_any_call('value_bar')
        mock_opened_file.write.assert_any_call('value_baz')
        mock_opened_file.write.assert_any_call('value_zom')
        self.assertEqual(mock_opened_file.write.call_count, 4)

        mock_print.assert_any_call('The following templates will be written:')
        mock_print.assert_any_call('outdir/subdir/name_foo')
        mock_print.assert_any_call('outdir/subdir/name_bar')
        mock_print.assert_any_call('outdir/subdir/nested/name_baz')
        mock_print.assert_any_call('outdir/subdir/nested/name_zom')
        self.assertEqual(mock_print.call_count, 5)
