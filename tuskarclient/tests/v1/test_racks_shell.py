#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import io
import mock

import tuskarclient.tests.utils as tutils
from tuskarclient.v1 import racks_shell


def empty_args():
    args = mock.Mock(spec=[])
    for attr in ['id', 'name', 'subnet', 'capacities', 'slots',
                 'resource_class']:
        setattr(args, attr, None)
    return args


def mock_rack():
    rack = mock.Mock()
    rack.id = '5'
    rack.name = 'test_rack'
    return rack


class RacksShellTest(tutils.TestCase):

    def setUp(self):
        self.outfile = io.StringIO()
        self.tuskar = mock.MagicMock()
        super(RacksShellTest, self).setUp()

    @mock.patch('tuskarclient.common.utils.find_resource')
    @mock.patch('tuskarclient.v1.racks_shell.print_rack_detail')
    def test_rack_show(self, mock_print_detail, mock_find_resource):
        mock_find_resource.return_value = mock_rack()
        args = empty_args()
        args.id = '5'

        racks_shell.do_rack_show(self.tuskar, args, outfile=self.outfile)
        mock_find_resource.assert_called_with(self.tuskar.racks, '5')
        mock_print_detail.assert_called_with(mock_find_resource.return_value,
                                             outfile=self.outfile)

    @mock.patch('tuskarclient.common.formatting.print_list')
    def test_rack_list(self, mock_print_list):
        args = empty_args()

        racks_shell.do_rack_list(self.tuskar, args, outfile=self.outfile)
        # testing the other arguments would be just copy-paste
        mock_print_list.assert_called_with(
            self.tuskar.racks.list.return_value, mock.ANY, mock.ANY, mock.ANY,
            outfile=self.outfile
        )

    @mock.patch('tuskarclient.common.utils.find_resource')
    @mock.patch('tuskarclient.v1.racks_shell.print_rack_detail')
    def test_rack_create(self, mock_print_detail, mock_find_resource):
        mock_find_resource.return_value = mock_rack()
        args = empty_args()
        args.name = 'my_rack'
        args.subnet = '1.2.3.4/20'
        args.capacities = 'total_memory:2048:MB,total_cpu:3:CPU'
        args.slots = '2'
        args.resource_class = '1'

        racks_shell.do_rack_create(self.tuskar, args, outfile=self.outfile)
        self.tuskar.racks.create.assert_called_with(
            name='my_rack',
            subnet='1.2.3.4/20',
            capacities=[
                {'name': 'total_memory', 'value': '2048', 'unit': 'MB'},
                {'name': 'total_cpu', 'value': '3', 'unit': 'CPU'}],
            slots='2',
            resource_class={'id': '1'})
        mock_print_detail.assert_called_with(
            self.tuskar.racks.create.return_value, outfile=self.outfile)

    @mock.patch('tuskarclient.common.utils.find_resource')
    @mock.patch('tuskarclient.v1.racks_shell.print_rack_detail')
    def test_rack_update(self, mock_print_detail, mock_find_resource):
        mock_find_resource.return_value = mock_rack()
        args = empty_args()
        args.id = '5'
        args.name = 'my_rack'
        args.capacities = 'total_memory:2048:MB,total_cpu:3:CPU'
        args.resource_class = '1'

        racks_shell.do_rack_update(self.tuskar, args, outfile=self.outfile)
        self.tuskar.racks.update.assert_called_with(
            '5',
            name='my_rack',
            capacities=[
                {'name': 'total_memory', 'value': '2048', 'unit': 'MB'},
                {'name': 'total_cpu', 'value': '3', 'unit': 'CPU'}],
            resource_class={'id': '1'})
        mock_print_detail.assert_called_with(
            self.tuskar.racks.update.return_value, outfile=self.outfile)

    @mock.patch('tuskarclient.common.utils.find_resource')
    def test_rack_delete(self, mock_find_resource):
        mock_find_resource.return_value = mock_rack()
        args = empty_args()
        args.id = '5'

        racks_shell.do_rack_delete(self.tuskar, args, outfile=self.outfile)
        self.tuskar.racks.delete.assert_called_with('5')
        self.assertEqual('Deleted rack "test_rack".\n',
                         self.outfile.getvalue())
