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
    },
    # rack
    {
        'commands': ['rack-delete -h',
                     'rack-delete --help',
                     'help rack-delete'],
        'test_identifiers': ['test_rack_delete_dash_h',
                             'test_rack_delete_dashdash_help',
                             'test_help_rack_delete'],
        'out_includes': [
            'usage: tuskar rack-delete [-h] <NAME or ID>',
            'positional arguments:',
            'optional arguments:',
            '<NAME or ID>',
        ],
        'out_excludes': [
            'rack-list',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
        ],
        'err_string': '',
        'return_code': 0,
    },
    {
        'commands': ['rack-update -h',
                     'rack-update --help',
                     'help rack-update'],
        'test_identifiers': ['test_rack_update_dash_h',
                             'test_rack_update_dashdash_help',
                             'test_help_rack_update'],
        'out_includes': [
            'usage: tuskar rack-update [-h] [--name NAME] [--subnet SUBNET]',
            'positional arguments:',
            '<NAME or ID>',
            'optional arguments:',
            '--name NAME',
            '--subnet SUBNET',
            '--slots SLOTS',
            '--capacities CAPACITIES',
            '--resource-class RESOURCE_CLASS',
        ],
        'out_excludes': [
            'rack-list',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
        ],
        'err_string': '',
        'return_code': 0,
    },
    {
        'commands': ['rack-create -h',
                     'rack-create --help',
                     'help rack-create'],
        'test_identifiers': ['test_rack_create_dash_h',
                             'test_rack_create_dashdash_help',
                             'test_help_rack_create'],
        'out_includes': [
            'usage: tuskar rack-create [-h] --subnet SUBNET --slots SLOTS',
            'positional arguments:',
            'optional arguments:',
            '--subnet SUBNET',
            '--slots SLOTS',
            '--capacities CAPACITIES',
            '--resource-class RESOURCE_CLASS',
        ],
        'out_excludes': [
            'rack-list',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
        ],
        'err_string': '',
        'return_code': 0,
    },
    {
        'commands': ['rack-show -h', 'rack-show --help', 'help rack-show'],
        'test_identifiers': ['test_rack_show_dash_h',
                             'test_rack_show_dashdash_help',
                             'test_help_rack_show'],
        'out_includes': [
            'usage: tuskar rack-show [-h] <NAME or ID>',
            'positional arguments:',
            'optional arguments:',
            '<NAME or ID>',
        ],
        'out_excludes': [
            'rack-list',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
        ],
        'err_string': '',
        'return_code': 0,
    },
    {
        'commands': ['rack-list -h', 'rack-list --help', 'help rack-list'],
        'test_identifiers': ['test_rack_list_dash_h',
                             'test_rack_list_dashdash_help',
                             'test_help_rack_list'],
        'out_includes': [
            'usage: tuskar rack-list [-h]',
            'optional arguments:',
        ],
        'out_excludes': [
            'rack-show',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
            'positional arguments:',
        ],
        'err_string': '',
        'return_code': 0,
    },
    # flavor
    {
        'commands': ['flavor-delete -h',
                     'flavor-delete --help',
                     'help flavor-delete'],
        'test_identifiers': ['test_flavor_delete_dash_h',
                             'test_flavor_delete_dashdash_help',
                             'test_help_flavor_delete'],
        'out_includes': [
            'usage: tuskar flavor-delete [-h]',
            'optional arguments:',
            'positional arguments:',
        ],
        'out_excludes': [
            'flavor-list',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
            '--capacities CAPACITIES',
        ],
        'err_string': '',
        'return_code': 0,
    },
    {
        'commands': ['flavor-update -h',
                     'flavor-update --help',
                     'help flavor-update'],
        'test_identifiers': ['test_flavor_update_dash_h',
                             'test_flavor_update_dashdash_help',
                             'test_help_flavor_update'],
        'out_includes': [
            'usage: tuskar flavor-update [-h] [--name NAME]'
            + ' [--capacities CAPACITIES]',
            'positional arguments:',
            'optional arguments:',
            '--capacities CAPACITIES',
            '--name NAME',
            '--max-vms MAX_VMS',
        ],
        'out_excludes': [
            'flavor-list',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
        ],
        'err_string': '',
        'return_code': 0,
    },
    {
        'commands': ['flavor-create -h',
                     'flavor-create --help',
                     'help flavor-create'],
        'test_identifiers': ['test_flavor_create_dash_h',
                             'test_flavor_create_dashdash_help',
                             'test_help_flavor_create'],
        'out_includes': [
            'usage:',
            'positional arguments:',
            'optional arguments:',
            '--capacities CAPACITIES',
        ],
        'out_excludes': [
            'flavor-list',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
        ],
        'err_string': '',
        'return_code': 0,
    },
    {
        'commands': ['flavor-show -h',
                     'flavor-show --help',
                     'help flavor-show'],
        'test_identifiers': ['test_flavor_show_dash_h',
                             'test_flavor_show_dashdash_help',
                             'test_help_flavor_show'],
        'out_includes': [
            'usage: tuskar flavor-show [-h] <RESOURCE CLASS NAME or ID>'
            + ' <FLAVOR NAME or ID>',
            'positional arguments:',
            'optional arguments:',
            'Name or ID of resource class associated to.',
        ],
        'out_excludes': [
            'flavor-list',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
            '--capacities CAPACITIES',
        ],
        'err_string': '',
        'return_code': 0,
    },
    {
        'commands': ['flavor-list -h',
                     'flavor-list --help',
                     'help flavor-list'],
        'test_identifiers': ['test_flavor_list_dash_h',
                             'test_flavor_list_dashdash_help',
                             'test_help_flavor_list'],
        'out_includes': [
            'usage: tuskar flavor-list [-h] <RESOURCE CLASS NAME or ID>',
            'positional arguments:',
            'optional arguments:',
        ],
        'out_excludes': [
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
            '--capacities CAPACITIES',
        ],
        'err_string': '',
        'return_code': 0,
    },
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
