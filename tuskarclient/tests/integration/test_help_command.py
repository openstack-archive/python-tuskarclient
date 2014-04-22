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
    # Overcloud Role - Create
    {
        'commands': ['overcloud-role-create -h',
                     'overcloud-role-create --help',
                     'help overcloud-role-create'],
        'test_identifiers': ['test_overcloud_role_create_dash_h',
                             'test_overcloud_role_create_dashdash_help',
                             'test_help_overcloud_role_create'],
        'out_includes': [
            '-d <DESCRIPTION>, --description <DESCRIPTION>',
            '-i <IMAGE NAME>, --image-name <IMAGE NAME>',
            '-f <FLAVOR ID>, --flavor-id <FLAVOR ID>'
        ],
        'out_excludes': [
            '-i <ID>, --id <ID>',
            'overcloud-role-list',
            'overcloud-create',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
        ],
        'err_string': '',
        'return_code': 0,
    },
    # Overcloud Role - Delete
    {
        'commands': ['overcloud-role-delete -h',
                     'overcloud-role-delete --help',
                     'help overcloud-role-delete'],
        'test_identifiers': ['test_overcloud_role_delete_dash_h',
                             'test_overcloud_role_delete_dashdash_help',
                             'test_help_overcloud_role_delete'],
        'out_includes': [
            '<ROLE>      ID or name of the Overcloud Role to delete.',
        ],
        'out_excludes': [
            'overcloud-role-list',
            'overcloud-delete',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
            '-d <DESCRIPTION>, --description <DESCRIPTION>',
            '-i <IMAGE NAME>, --image-name <IMAGE NAME>',
            '-f <FLAVOR ID>, --flavor-id <FLAVOR ID>'
        ],
        'err_string': '',
        'return_code': 0,
    },
    # Overcloud Role - List
    {
        'commands': ['overcloud-role-list -h',
                     'overcloud-role-list --help',
                     'help overcloud-role-list'],
        'test_identifiers': ['test_overcloud_role_list_dash_h',
                             'test_overcloud_role_list_dashdash_help',
                             'test_help_overcloud_role_list'],
        'out_includes': [
        ],
        'out_excludes': [
            'overcloud-role-delete',
            'overcloud-list',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
            '-n <NAME>, --name <NAME>',
            '-d <DESCRIPTION>, --description <DESCRIPTION>',
            '-i <IMAGE NAME>, --image-name <IMAGE NAME>',
            '-f <FLAVOR ID>, --flavor-id <FLAVOR ID>'
        ],
        'err_string': '',
        'return_code': 0,
    },
    # Overcloud Role - Show
    {
        'commands': ['overcloud-role-show -h',
                     'overcloud-role-show --help',
                     'help overcloud-role-show'],
        'test_identifiers': ['test_overcloud_role_show_dash_h',
                             'test_overcloud_role_show_dashdash_help',
                             'test_help_overcloud_role_show'],
        'out_includes': [
            '<ROLE>      ID or name of the Overcloud Role to show.',
        ],
        'out_excludes': [
            'overcloud-role-list',
            'overcloud-show',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
        ],
        'err_string': '',
        'return_code': 0,
    },
    # Overcloud Role - Update
    {
        'commands': ['overcloud-role-update -h',
                     'overcloud-role-update --help',
                     'help overcloud-role-update'],
        'test_identifiers': ['test_overcloud_role_update_dash_h',
                             'test_overcloud_role_update_dashdash_help',
                             'test_help_overcloud_role_update'],
        'out_includes': [
            '-n <NAME>, --name <NAME>',
            '-d <DESCRIPTION>, --description <DESCRIPTION>',
            '-i <IMAGE NAME>, --image-name <IMAGE NAME>',
            '-f <FLAVOR ID>, --flavor-id <FLAVOR ID>'
        ],
        'out_excludes': [
            'overcloud-role-list',
            'overcloud-update',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
        ],
        'err_string': '',
        'return_code': 0,
    },
    # Overcloud - Create
    {
        'commands': ['overcloud-create -h',
                     'overcloud-create --help',
                     'help overcloud-create'],
        'test_identifiers': ['test_overcloud_create_dash_h',
                             'test_overcloud_create_dashdash_help',
                             'test_help_overcloud_create'],
        'out_includes': [
        ],
        'out_excludes': [
            '-i <ID>, --id <ID>',
            'overcloud-list',
            'overcloud-role-create',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
        ],
        'err_string': '',
        'return_code': 0,
    },
    # Overcloud - Delete
    {
        'commands': ['overcloud-delete -h',
                     'overcloud-delete --help',
                     'help overcloud-delete'],
        'test_identifiers': ['test_overcloud_delete_dash_h',
                             'test_overcloud_delete_dashdash_help',
                             'test_help_overcloud_delete'],
        'out_includes': [
            '<OVERCLOUD>  ID or name of the Overcloud to delete.',
        ],
        'out_excludes': [
            'overcloud-list',
            'overcloud-role-delete',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
            '-d <DESCRIPTION>, --description <DESCRIPTION>',
            '-i <IMAGE NAME>, --image-name <IMAGE NAME>',
            '-f <FLAVOR ID>, --flavor-id <FLAVOR ID>'
        ],
        'err_string': '',
        'return_code': 0,
    },
    # Overcloud - List
    {
        'commands': ['overcloud-list -h',
                     'overcloud-list --help',
                     'help overcloud-list'],
        'test_identifiers': ['test_overcloud_list_dash_h',
                             'test_overcloud_list_dashdash_help',
                             'test_help_overcloud_list'],
        'out_includes': [
        ],
        'out_excludes': [
            'overcloud-delete',
            'overcloud-role-list',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
            '-n <NAME>, --name <NAME>',
            '-d <DESCRIPTION>, --description <DESCRIPTION>',
            '-i <IMAGE NAME>, --image-name <IMAGE NAME>',
            '-f <FLAVOR ID>, --flavor-id <FLAVOR ID>'
        ],
        'err_string': '',
        'return_code': 0,
    },
    # Overcloud - Show
    {
        'commands': ['overcloud-show -h',
                     'overcloud-show --help',
                     'help overcloud-show'],
        'test_identifiers': ['test_overcloud_show_dash_h',
                             'test_overcloud_show_dashdash_help',
                             'test_help_overcloud_show'],
        'out_includes': [
            '<OVERCLOUD>  ID or name of the Overcloud to show.',
        ],
        'out_excludes': [
            'overcloud-list',
            'overcloud-role-show',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
        ],
        'err_string': '',
        'return_code': 0,
    },
    # Overcloud - Update
    {
        'commands': ['overcloud-update -h',
                     'overcloud-update --help',
                     'help overcloud-update'],
        'test_identifiers': ['test_overcloud_update_dash_h',
                             'test_overcloud_update_dashdash_help',
                             'test_help_overcloud_update'],
        'out_includes': [
            '-n <NAME>, --name <NAME>'
        ],
        'out_excludes': [
            'overcloud-list',
            'overcloud-role-update',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
        ],
        'err_string': '',
        'return_code': 0,
    },
    # Overcloud - show template parameters
    {
        'commands': ['overcloud-show-template-parameters -h',
                     'overcloud-show-template-parameters --help',
                     'help overcloud-show-template-parameters'],
        'test_identifiers': [
            'test_overcloud_show_template_parameters_dash_h',
            'test_overcloud_show_template_parameters_dashdash_help',
            'test_help_overcloud_show_template_parameters'
        ],
        'out_includes': [
            'Show the template parameters stored in the Tuskar API.'
        ],
        'out_excludes': [
            '-n <NAME>, --name <NAME>'
            'overcloud-list',
            'overcloud-role-template-parameters',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
        ],
        'err_string': '',
        'return_code': 0,
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

# Create a method for each command found in the above tests. The tests will be
# constructed on the HelpCommandTest class with the name given in the test
# identifiers. This way the developer can search the above structure for the
# identifier and find the actual data used in the test.
duplicated = []

for test in tests:
    commands = test.get('commands')
    for index, command in enumerate(commands):
        test_command_method = create_test_method(command, test)
        test_command_method.__name__ = test.get('test_identifiers')[index]

        if hasattr(HelpCommandTest, test_command_method.__name__):
            duplicated.append(test_command_method.__name__)

        setattr(HelpCommandTest,
                test_command_method.__name__,
                test_command_method)


# Finally add a meta test to verify that no test identifiers were used twice
# which would result in only the last test being added.
def _meta_verify_test_builder(self):
    self.assertEqual(
        duplicated, [], "Expected no test identifiers to be "
        "duplicated but found {0}".format(len(duplicated))
    )

setattr(HelpCommandTest, 'test_test_builder_for_duplicates',
        _meta_verify_test_builder)
