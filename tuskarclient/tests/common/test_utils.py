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


import cStringIO
import mock
import sys

from tuskarclient.common import utils
from tuskarclient.tests import utils as test_utils


class UtilsTest(test_utils.TestCase):

    def test_prettytable(self):
        class Struct:
            def __init__(self, **entries):
                self.__dict__.update(entries)

        # test that the prettytable output is wellformatted (left-aligned)
        saved_stdout = sys.stdout
        try:
            sys.stdout = output_dict = cStringIO.StringIO()
            utils.print_dict({'K': 'k', 'Key': 'Value'})

        finally:
            sys.stdout = saved_stdout

        self.assertEqual(output_dict.getvalue(), '''\
+----------+-------+
| Property | Value |
+----------+-------+
| K        | k     |
| Key      | Value |
+----------+-------+
''')


class DefineCommandsTest(test_utils.TestCase):

    def test_define_commands_from_module(self):
        subparsers = mock.Mock()
        subparser = mock.MagicMock()
        subparsers.add_parser.return_value = subparser
        dummy_module = self.dummy_command_module()

        utils.define_commands_from_module(subparsers, dummy_module)
        subparsers.add_parser.assert_called_with(
            'dummy-list', help="Docstring", description="Docstring")
        subparser.add_argument.assert_called_with(
            '-a', metavar='<NUMBER>', help="Add a number.")
        subparser.set_defaults.assert_called_with(
            func=dummy_module.do_dummy_list)

    def dummy_command_module(self):
        @utils.arg('-a', metavar='<NUMBER>', help="Add a number.")
        def do_dummy_list():
            '''Docstring'''
            return 42

        dummy = mock.Mock()
        dummy.do_dummy_list = do_dummy_list
        dummy.other_method = mock.Mock('other_method', return_value=43)
        return dummy
