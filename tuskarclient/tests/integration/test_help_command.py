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
    def test_bare_help(self):
        results = self.run_tuskar('help')
        out_includes = [
            'usage:',
            'positional arguments:',
            'optional arguments:',
        ]
        self.assertThat(
            results,
            tutils.CommandOutputMatches(
                out_inc=out_includes,
                err_str='',
                return_code=0,
            ))

    def test_help_with_h(self):
        self.help_for_help_test('help -h')

    def test_help_with_help(self):
        self.help_for_help_test('help --help')

    def test_help_help(self):
        self.help_for_help_test('help help')

    def help_for_help_test(self, command):
        results = self.run_tuskar(command)
        out_includes = [
            'usage:',
            'positional arguments:',
            'optional arguments:',
            'Display help for <subcommand>',
        ]
        out_excludes = [
            'flavor-list',
            '--os-username OS_USERNAME',
        ]
        self.assertThat(
            results,
            tutils.CommandOutputMatches(
                out_inc=out_includes,
                out_exc=out_excludes,
                err_str='',
                return_code=0,
            ))

    def test_help_with_bad_argument(self):
        results = self.run_tuskar('help -r')
        err_includes = [
            'error: unrecognized arguments: -r',
        ]
        self.assertThat(
            results,
            tutils.CommandOutputMatches(
                out_str='',
                err_inc=err_includes,
                return_code=2,
            ))
