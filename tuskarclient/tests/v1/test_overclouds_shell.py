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

from tuskarclient.openstack.common.apiclient import exceptions
import tuskarclient.tests.utils as tutils
from tuskarclient.v1.overcloud_roles import OvercloudRole
from tuskarclient.v1 import overclouds_shell


def empty_args():
    args = mock.Mock(spec=[])
    for attr in ['id', 'name', 'subnet', 'capacities', 'slots',
                 'resource_class']:
        setattr(args, attr, None)
    return args


def mock_overcloud():
    overcloud = mock.Mock()
    overcloud.id = '5'
    overcloud.name = 'My Overcloud'
    return overcloud


class BaseOvercloudShellTest(tutils.TestCase):

    def setUp(self):
        super(BaseOvercloudShellTest, self).setUp()
        self.outfile = six.StringIO()
        self.tuskar = mock.MagicMock()
        self.shell = overclouds_shell


class OvercloudShellTest(BaseOvercloudShellTest):

    @mock.patch('tuskarclient.common.utils.find_resource')
    @mock.patch('tuskarclient.v1.overclouds_shell.print_overcloud_detail')
    def test_overcloud_show(self, mock_print_detail, mock_find_resource):
        mock_find_resource.return_value = mock_overcloud()
        args = empty_args()
        args.overcloud = '5'

        self.shell.do_overcloud_show(self.tuskar, args, outfile=self.outfile)
        mock_find_resource.assert_called_with(self.tuskar.overclouds, '5')
        mock_print_detail.assert_called_with(mock_find_resource.return_value,
                                             outfile=self.outfile)

    @mock.patch('tuskarclient.common.formatting.print_list')
    def test_overcloud_list(self, mock_print_list):
        args = empty_args()

        self.shell.do_overcloud_list(self.tuskar, args, outfile=self.outfile)
        # testing the other arguments would be just copy-paste
        mock_print_list.assert_called_with(
            self.tuskar.overclouds.list.return_value, mock.ANY, mock.ANY,
            outfile=self.outfile
        )

    @mock.patch('tuskarclient.v1.overclouds_shell.print_overcloud_detail')
    def test_overcloud_create(self, mock_print_detail):
        args = empty_args()
        args.name = 'my_overcloud'
        args.attributes = None
        args.roles = None

        self.shell.do_overcloud_create(self.tuskar, args, outfile=self.outfile)
        self.tuskar.overclouds.create.assert_called_with(
            name='my_overcloud',
            counts=[],
            attributes={}
        )
        mock_print_detail.assert_called_with(
            self.tuskar.overclouds.create.return_value, outfile=self.outfile)

    @mock.patch('tuskarclient.common.utils.find_resource')
    @mock.patch('tuskarclient.v1.overclouds_shell.print_overcloud_detail')
    def test_overcloud_update(self, mock_print_detail, mock_find_resource):
        mock_find_resource.return_value = mock_overcloud()
        args = empty_args()
        args.overcloud = '5'
        args.name = 'my_overcloud'
        args.attributes = None
        args.roles = None

        self.shell.do_overcloud_update(self.tuskar, args, outfile=self.outfile)
        self.tuskar.overclouds.update.assert_called_with(
            '5',
            name='my_overcloud',
            attributes={},
            counts=[]
        )
        mock_print_detail.assert_called_with(
            self.tuskar.overclouds.update.return_value, outfile=self.outfile)

    @mock.patch('tuskarclient.common.utils.find_resource')
    def test_overcloud_delete(self, mock_find_resource):
        mock_find_resource.return_value = mock_overcloud()
        args = empty_args()
        args.overcloud = '5'

        self.shell.do_overcloud_delete(self.tuskar, args, outfile=self.outfile)
        self.tuskar.overclouds.delete.assert_called_with('5')
        self.assertEqual('Deleted Overcloud "My Overcloud".\n',
                         self.outfile.getvalue())


class OvercloudAttributeShellTest(BaseOvercloudShellTest):

    def setUp(self):
        super(OvercloudAttributeShellTest, self).setUp()

        self.args = empty_args()
        self.args.name = 'my_overcloud'
        self.args.roles = None
        self.create = self.shell.do_overcloud_create

    @mock.patch('tuskarclient.v1.overclouds_shell.print_overcloud_detail')
    def test_create_attributes(self, mock_print_detail):
        self.args.attributes = ['val1=10', 'val2=20', 'val3=30']

        self.create(self.tuskar, self.args, outfile=self.outfile)
        self.tuskar.overclouds.create.assert_called_with(
            name='my_overcloud',
            counts=[],
            attributes={
                'val1': '10',
                'val2': '20',
                'val3': '30',
            }
        )
        mock_print_detail.assert_called_with(
            self.tuskar.overclouds.create.return_value, outfile=self.outfile)

    @mock.patch('tuskarclient.v1.overclouds_shell.print_overcloud_detail')
    def test_create_attributes_duplicate(self, mock_print_detail):
        self.args.attributes = ['val1=10', 'val1=20']

        self.assertRaises(
            exceptions.ValidationError,
            self.create,
            self.tuskar, self.args, outfile=self.outfile)

        self.tuskar.overclouds.create.assert_not_called()

    @mock.patch('tuskarclient.v1.overclouds_shell.print_overcloud_detail')
    def test_create_attributes_invalid(self, mock_print_detail):
        self.args.attributes = ['val1=10', 'val120']

        self.assertRaises(
            exceptions.CommandError,
            self.create,
            self.tuskar, self.args, outfile=self.outfile)

        self.tuskar.overclouds.create.assert_not_called()

    @mock.patch('tuskarclient.v1.overclouds_shell.print_overcloud_detail')
    def test_create_attributes_multiple_equals(self, mock_print_detail):
        self.args.attributes = ['val1=10', 'val2=2=0']

        self.create(self.tuskar, self.args, outfile=self.outfile)
        self.tuskar.overclouds.create.assert_called_with(
            name='my_overcloud',
            counts=[],
            attributes={
                'val1': '10',
                'val2': '2=0',
            }
        )
        mock_print_detail.assert_called_with(
            self.tuskar.overclouds.create.return_value, outfile=self.outfile)


class OvercloudRoleShellTest(BaseOvercloudShellTest):

    def setUp(self):
        super(OvercloudRoleShellTest, self).setUp()

        self.args = empty_args()
        self.args.name = 'my_overcloud'
        self.args.attributes = None
        self.create = self.shell.do_overcloud_create

    @mock.patch('tuskarclient.v1.overclouds_shell.print_overcloud_detail')
    def test_create_roles(self, mock_print_detail):
        self.args.roles = ['foo=10']
        self.tuskar.overcloud_roles.list.return_value =\
            [OvercloudRole(None, {'name': 'foo', 'id': 1})]

        self.create(self.tuskar, self.args, outfile=self.outfile)
        self.tuskar.overclouds.create.assert_called_with(
            name='my_overcloud',
            attributes={},
            counts=[
                {'overcloud_role_id': 1, 'num_nodes': 10},
            ]
        )
        mock_print_detail.assert_called_with(
            self.tuskar.overclouds.create.return_value, outfile=self.outfile)

    @mock.patch('tuskarclient.v1.overclouds_shell.print_overcloud_detail')
    def test_create_roles_duplicate(self, mock_print_detail):
        self.args.roles = ['foo=10', 'foo=20']
        self.tuskar.overcloud_roles.list.return_value =\
            [OvercloudRole(None, {'name': 'foo', 'id': 1})]

        self.assertRaises(
            exceptions.ValidationError,
            self.create,
            self.tuskar, self.args, outfile=self.outfile)

        self.tuskar.overclouds.create.assert_not_called()

    @mock.patch('tuskarclient.v1.overclouds_shell.print_overcloud_detail')
    def test_create_roles_invalid_structure(self, mock_print_detail):
        self.args.roles = ['foo=10', '120']
        self.tuskar.overcloud_roles.list.return_value =\
            [OvercloudRole(None, {'name': 'foo', 'id': 1})]

        self.assertRaises(
            exceptions.CommandError,
            self.create,
            self.tuskar, self.args, outfile=self.outfile)

        self.tuskar.overclouds.create.assert_not_called()

    @mock.patch('tuskarclient.v1.overclouds_shell.print_overcloud_detail')
    def test_create_roles_multiple_equals(self, mock_print_detail):
        self.args.roles = ['foo=foo=0']
        self.tuskar.overcloud_roles.list.return_value =\
            [OvercloudRole(None, {'name': 'foo', 'id': 1})]

        self.assertRaises(
            ValueError,
            self.create,
            self.tuskar, self.args, outfile=self.outfile)

        self.tuskar.overclouds.create.assert_not_called()

    @mock.patch('tuskarclient.v1.overclouds_shell.print_overcloud_detail')
    def test_create_roles_with_id(self, mock_print_detail):
        self.args.roles = ['12345=10']
        self.tuskar.overcloud_roles.list.return_value =\
            [OvercloudRole(None, {'name': 'foo', 'id': 1})]

        self.create(self.tuskar, self.args, outfile=self.outfile)
        self.tuskar.overclouds.create.assert_called_with(
            name='my_overcloud',
            attributes={},
            counts=[
                {'overcloud_role_id': '12345', 'num_nodes': 10},
            ]
        )
        mock_print_detail.assert_called_with(
            self.tuskar.overclouds.create.return_value, outfile=self.outfile)
