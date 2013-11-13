
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


class HelpFlavorUpdateTest(tutils.CommandTestCase):
    def test_flavor_update_with_h(self):
        self.help_for_flavor_update_test('flavor-update -h')

    def test_flavor_update_with_help(self):
        self.help_for_flavor_update_test('flavor-update --help')

    def test_help_flavor_create(self):
        self.help_for_flavor_update_test('help flavor-update')

    def help_for_flavor_update_test(self, command):
        results = self.run_tuskar(command)
        out_includes = [
            'usage: tuskar flavor-update [-h] [--name NAME]'
            + ' [--capacities CAPACITIES]',
            'positional arguments:',
            'optional arguments:',
            '--capacities CAPACITIES',
            '--name NAME',
            '--max-vms MAX_VMS',
        ]
        out_excludes = [
            'flavor-list',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
        ]
        self.assertThat(
            results,
            tutils.CommandOutputMatches(
                out_inc=out_includes,
                out_exc=out_excludes,
                err_str='',
                return_code=0,
            ))
