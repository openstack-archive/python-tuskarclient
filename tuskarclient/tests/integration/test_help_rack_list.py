
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


class HelpRackListTest(tutils.CommandTestCase):
    def test_rack_list_with_h(self):
        self.help_for_rack_list_test('rack-list -h')

    def test_rack_list_with_help(self):
        self.help_for_rack_list_test('rack-list --help')

    def test_help_rack_create(self):
        self.help_for_rack_list_test('help rack-list')

    def help_for_rack_list_test(self, command):
        results = self.run_tuskar(command)
        out_includes = [
            'usage: tuskar rack-list [-h]',
            'optional arguments:',
        ]
        out_excludes = [
            'rack-show',
            '--os-username OS_USERNAME',
            'Display help for <subcommand>',
            'positional arguments:',
        ]
        self.assertThat(
            results,
            tutils.CommandOutput(
                out_inc=out_includes,
                out_exc=out_excludes,
                err_str='',
                return_code=0,
            ))
