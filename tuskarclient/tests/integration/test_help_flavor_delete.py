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


class HelpFlavorDeleteTest(tutils.CommandTestCase):
    def test_flavor_delete_with_h(self):
        self.help_for_flavor_delete_test('flavor-delete -h')

    def test_flavor_delete_with_help(self):
        self.help_for_flavor_delete_test('flavor-delete --help')

    def test_help_flavor_create(self):
        self.help_for_flavor_delete_test('help flavor-delete')

    def help_for_flavor_delete_test(self, command):
        results = self.run_tuskar(command)
        out_includes = [
            'usage: tuskar flavor-delete [-h]',
            'optional arguments:',
            'positional arguments:',
        ]
        out_excludes = [
            'flavor-list',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
            '--capacities CAPACITIES',
        ]
        self.assertThat(
            results,
            tutils.CommandOutput(
                out_inc=out_includes,
                out_exc=out_excludes,
                err_str='',
                return_code=0,
            ))
