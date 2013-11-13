
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


class HelpRackDeleteTest(tutils.CommandTestCase):
    def test_rack_delete_with_h(self):
        self.help_for_rack_delete_test('rack-delete -h')

    def test_rack_delete_with_help(self):
        self.help_for_rack_delete_test('rack-delete --help')

    def test_help_rack_create(self):
        self.help_for_rack_delete_test('help rack-delete')

    def help_for_rack_delete_test(self, command):
        results = self.run_tuskar(command)
        out_includes = [
            'usage: tuskar rack-delete [-h] <NAME or ID>',
            'positional arguments:',
            'optional arguments:',
            '<NAME or ID>',
        ]
        out_excludes = [
            'rack-list',
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
