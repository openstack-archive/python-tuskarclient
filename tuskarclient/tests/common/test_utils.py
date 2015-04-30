# Copyright 2013 OpenStack LLC.
# All Rights Reserved.
#
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


import mock

from tuskarclient.common import utils
from tuskarclient.openstack.common.apiclient import exceptions as exc
from tuskarclient.tests import utils as test_utils


class DefineCommandsTest(test_utils.TestCase):

    def test_define_commands_from_module(self):
        subparsers = mock.Mock()
        subparser = mock.MagicMock()
        subparsers.add_parser.return_value = subparser
        dummy_module = self.dummy_command_module()

        utils.define_commands_from_module(subparsers, dummy_module)
        subparsers.add_parser.assert_called_with(
            'dummy-list', help="Docstring.", description="Docstring.")
        subparser.add_argument.assert_called_with(
            '-a', metavar='<NUMBER>', help="Add a number.")
        subparser.set_defaults.assert_called_with(
            func=dummy_module.do_dummy_list)

    def dummy_command_module(self):
        @utils.arg('-a', metavar='<NUMBER>', help="Add a number.")
        def do_dummy_list():
            '''Docstring.'''
            return 42

        dummy = mock.Mock()
        dummy.do_dummy_list = do_dummy_list
        dummy.other_method = mock.Mock('other_method', return_value=43)
        return dummy


class FindResourceTest(test_utils.TestCase):

    def setUp(self):
        super(FindResourceTest, self).setUp()

        self.overcloud1 = mock.Mock()
        self.overcloud1.id = '1'
        self.overcloud1.name = 'My Overcloud 1'

        self.overcloud2 = mock.Mock()
        self.overcloud2.id = '2'
        self.overcloud2.name = 'My Overcloud 2'

        self.overcloud3 = mock.Mock()
        self.overcloud3.id = '3'
        self.overcloud3.name = 'My Overcloud 2'

        self.manager = mock.Mock()
        self.manager.resource_class = None
        self.manager.get.return_value = self.overcloud1
        self.manager.resource_class = mock.Mock(__name__='Overcloud',
                                                NAME_ATTR='name')
        self.manager.list.return_value = [
            self.overcloud1,
            self.overcloud2,
            self.overcloud3]

    def test_with_id(self):
        overcloud = utils.find_resource(self.manager, '1')
        self.manager.get.assert_called_with(1)
        self.assertEqual(self.overcloud1, overcloud)

    def test_with_name(self):
        overcloud = utils.find_resource(self.manager, 'My Overcloud 1')
        self.assertEqual(self.overcloud1, overcloud)

    def test_no_match(self):
        self.assertRaises(exc.CommandError,
                          utils.find_resource,
                          self.manager,
                          'My Overcloud 3')

    def test_multiple_matches(self):
        self.assertRaises(exc.CommandError,
                          utils.find_resource,
                          self.manager,
                          'My Overcloud 2')


class ParseCLIArgsTest(test_utils.TestCase):

    def setUp(self):
        super(ParseCLIArgsTest, self).setUp()

        self.mock_role1 = mock.Mock()
        self.mock_role1.configure_mock(name="role1", version=1)

        self.mock_role2 = mock.Mock()
        self.mock_role2.configure_mock(name="role2", version=2)

        self.roles = [self.mock_role1, self.mock_role2]

    def test_parameters_args_to_patch(self):

        args = [
            "parameter1=value1",
            "parameter2=value2",
        ]

        result = utils.parameters_args_to_patch(args)

        self.assertEqual([
            {'name': 'parameter1', 'value': 'value1'},
            {'name': 'parameter2', 'value': 'value2'},
        ], result)

    def test_flavors_args_to_patch(self):

        args = [
            "role1-1=flavor1",
            "role2-2=flavor2",
        ]

        result = utils.args_to_patch(args, self.roles, "Flavor")

        self.assertEqual([
            {'name': 'role1-1::Flavor', 'value': 'flavor1'},
            {'name': 'role2-2::Flavor', 'value': 'flavor2'}
        ], result)

    def test_scale_args_to_patch(self):

        args = [
            "role1-1=1",
            "role2-2=2",
        ]

        result = utils.args_to_patch(args, self.roles, "count")

        self.assertEqual([
            {'name': 'role1-1::count', 'value': '1'},
            {'name': 'role2-2::count', 'value': '2'}
        ], result)
