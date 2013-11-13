
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


class HelpFlavorListTest(tutils.CommandTestCase):
    def test_flavor_list_with_h(self):
        self.help_for_flavor_list_test('flavor-list -h')

    def test_flavor_list_with_help(self):
        self.help_for_flavor_list_test('flavor-list --help')

    def test_help_flavor_create(self):
        self.help_for_flavor_list_test('help flavor-list')

    def help_for_flavor_list_test(self, command):
        results = self.run_tuskar(command)
        out_includes = [
            'usage: tuskar flavor-list [-h] <RESOURCE CLASS NAME or ID>',
            'positional arguments:',
            'optional arguments:',
        ]
        out_excludes = [
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
            '--capacities CAPACITIES',
        ]
        self.assertThat(
            results,
            tutils.CommandOutputMatches(
                out_inc=out_includes,
                out_exc=out_excludes,
                err_str='',
                return_code=0,
            ))
