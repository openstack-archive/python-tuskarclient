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
from tuskarclient.v1 import overcloud_roles_shell


def empty_args():
    args = mock.Mock(spec=[])
    for attr in ['id', 'name', 'subnet', 'capacities', 'slots',
                 'resource_class']:
        setattr(args, attr, None)
    return args


def mock_overcloud():
    overcloud = mock.Mock()
    overcloud.id = '5'
    overcloud.name = 'Testing Overcloud Role'
    return overcloud


class OvercloudRoleShellTest(tutils.TestCase):

    def setUp(self):
        super(OvercloudRoleShellTest, self).setUp()
        self.outfile = six.StringIO()
        self.tuskar = mock.MagicMock()
        self.shell = overcloud_roles_shell

    @mock.patch('tuskarclient.common.utils.find_resource')
    @mock.patch('tuskarclient.v1.overcloud_roles_shell.print_role_detail')
    def test_overcloud_role_show(self, mock_print_detail, mock_find_resource):
        mock_find_resource.return_value = mock_overcloud()
        args = empty_args()
        args.role = '5'

        self.shell.do_overcloud_role_show(self.tuskar, args,
                                          outfile=self.outfile)
        mock_find_resource.assert_called_with(self.tuskar.overcloud_roles, '5')
        mock_print_detail.assert_called_with(mock_find_resource.return_value,
                                             outfile=self.outfile)

    @mock.patch('tuskarclient.common.formatting.print_list')
    def test_overcloud_role_list(self, mock_print_list):
        args = empty_args()

        self.shell.do_overcloud_role_list(self.tuskar, args,
                                          outfile=self.outfile)
        # testing the other arguments would be just copy-paste
        mock_print_list.assert_called_with(
            self.tuskar.overcloud_roles.list.return_value, mock.ANY,
            outfile=self.outfile
        )

    @mock.patch('tuskarclient.common.utils.find_resource')
    @mock.patch('tuskarclient.v1.overcloud_roles_shell.print_role_detail')
    def test_overcloud_role_create(self, mock_print, mock_find_resource):
        mock_find_resource.return_value = mock_overcloud()
        args = empty_args()
        args.name = 'My Overcloud Role'
        args.description = 'This is an Overcloud Role.'
        args.image_name = 'image'
        args.flavor_id = '1'

        self.shell.do_overcloud_role_create(self.tuskar, args,
                                            outfile=self.outfile)
        self.tuskar.overcloud_roles.create.assert_called_with(
            name='My Overcloud Role',
            flavor_id='1',
            description='This is an Overcloud Role.',
            image_name='image'
        )
        mock_print.assert_called_with(
            self.tuskar.overcloud_roles.create.return_value,
            outfile=self.outfile
        )

    @mock.patch('tuskarclient.common.utils.find_resource')
    @mock.patch('tuskarclient.v1.overcloud_roles_shell.print_role_detail')
    def test_overcloud_role_update(self, mock_print, mock_find_resource):
        mock_find_resource.return_value = mock_overcloud()
        args = empty_args()
        args.role = '5'
        args.name = 'My Overcloud Role'
        args.description = 'This is an Overcloud Role.'
        args.image_name = 'image'
        args.flavor_id = '1'

        self.shell.do_overcloud_role_update(self.tuskar, args,
                                            outfile=self.outfile)
        self.tuskar.overcloud_roles.update.assert_called_with(
            '5',
            name='My Overcloud Role',
            flavor_id='1',
            description='This is an Overcloud Role.',
            image_name='image'
        )
        mock_print.assert_called_with(
            self.tuskar.overcloud_roles.update.return_value,
            outfile=self.outfile
        )

    @mock.patch('tuskarclient.common.utils.find_resource')
    def test_overcloud_role_delete(self, mock_find_resource):
        mock_find_resource.return_value = mock_overcloud()
        args = empty_args()
        args.role = '5'

        self.shell.do_overcloud_role_delete(self.tuskar, args,
                                            outfile=self.outfile)
        self.tuskar.overcloud_roles.delete.assert_called_with('5')
        self.assertEqual('Deleted Overcloud Role "Testing Overcloud Role".\n',
                         self.outfile.getvalue())
