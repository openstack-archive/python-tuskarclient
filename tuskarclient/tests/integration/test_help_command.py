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

import tuskarclient.tests.utils as tutils


class HelpCommandTest(tutils.CommandTestCase):
    pass

tests = [
    # help
    {
        'commands': ['help'],  # commands to test "tuskar help"
        # helps find failed tests in code - needs "test_" prefix
        'test_identifiers': ['test_help'],
        'out_includes': [  # what should be in output
            'usage:',
            'positional arguments:',
            'optional arguments:',
        ],
        'out_excludes': [  # what should not be in output
            'foo bar baz',
        ],
        'err_string': '',  # how error output should look like
        'return_code': 0,
    },
    {
        'commands': ['help -h', 'help --help', 'help help'],
        'test_identifiers': ['test_help_dash_h',
                             'test_help_dashdash_help',
                             'test_help_help'],
        'out_includes': [
            'usage:',
            'positional arguments:',
            'optional arguments:',
            'Display help for <subcommand>',
        ],
        'out_excludes': [
            'flavor-list',
            '--os-username OS_USERNAME',
        ],
        'err_string': '',
        'return_code': 0,
    },
    {
        'commands': ['help -r'],
        'test_identifiers': ['test_help_dash_r'],
        'out_string': '',
        'err_includes': [
            'error: unrecognized arguments: -r',
        ],
        'return_code': 2,
    }
]


def create_test_method(command, expected_values):
    def test_command_method(self):
        self.assertThat(
            self.run_tuskar(command),
            tutils.CommandOutputMatches(
                out_str=expected_values.get('out_string'),
                out_inc=expected_values.get('out_includes'),
                out_exc=expected_values.get('out_excludes'),
                err_str=expected_values.get('err_string'),
                err_inc=expected_values.get('err_includes'),
                err_exc=expected_values.get('err_excludes'),
            ))
    return test_command_method

# creates a method for each command found in tests
# to let developer see what test is failing in test results,
# ie: ... HelpCommandTest.test_help_flavor_list
# this way dev can "just search" for "test_help_flavor_list"
# and he will find actual data used in failing test
for test in tests:
    commands = test.get('commands')
    for index, command in enumerate(commands):
        test_command_method = create_test_method(command, test)
        test_command_method.__name__ = test.get('test_identifiers')[index]
        setattr(HelpCommandTest,
                test_command_method.__name__,
                test_command_method)
