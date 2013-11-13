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


class CommandOutput(object):
    def __init__(self,
                 out_str=None, out_inc=[], out_exc=[],
                 err_str=None, err_inc=[], err_exc=[]):
        self.out_str = out_str
        self.out_inc = out_inc
        self.out_exc = out_exc
        self.err_str = err_str
        self.err_inc = err_inc
        self.err_exc = err_exc

    def match(self, outputs):
        out, err = outputs[0], outputs[1]
        if self.out_str:
            if self.out_str == out:
                return CommandOutputMismatch(out, self.out_str, type='output')
        for part in self.out_inc:
            if part not in out:
                return CommandOutputMissingMismatch(out, part, type='output')
        for part in self.out_exc:
            if part in out:
                return CommandOutputExtraMismatch(out, part, type='output')
        if self.err_str:
            if self.err_str == err:
                return CommandOutputMismatch(err, self.err_str, type='error')
        for part in self.err_inc:
            if part not in err:
                return CommandOutputMissingMismatch(err, part, type='error')
        for part in self.err_exc:
            if part in err:
                return CommandOutputExtraMismatch(err, part, type='error')
        return None


class CommandOutputMismatch(object):
    def __init__(self, out, out_str, type='output'):
        if type == 'error':
            self.type = 'Error output'
        else:
            self.type = 'Output'
        self.out = out
        self.out_str = out_str

    def describe(self):
        return "%s '%s' should be '%s'" % (self.type, self.out, self.out_str)

    def get_details(self):
        return {}


class CommandOutputMissingMismatch(object):
    def __init__(self, out, out_inc, type='output'):
        if type == 'error':
            self.type = 'Error output'
        else:
            self.type = 'Output'
        self.out = out
        self.out_inc = out_inc

    def describe(self):
        return "%s '%s' should contain '%s'"\
            % (self.type, self.out, self.out_inc)

    def get_details(self):
        return {}


class CommandOutputExtraMismatch(object):
    def __init__(self, out, out_exc, type='output'):
        if type == 'error':
            self.type = 'Error output'
        else:
            self.type = 'Output'
        self.out = out
        self.out_exc = out_exc

    def describe(self):
        return "%s '%s' should not contain '%s'"\
            % (self.type, self.out, self.out_exc)

    def get_details(self):
        return {}


class HelpCommandTest(tutils.CommandTestCase):
    def test_bare_help(self):
        out, err = self.run_tuskar('help')
        out_includes = [
            'usage:',
            'positional arguments:',
            'optional arguments:',
        ]
        self.assertThat(
            [out, err],
            CommandOutput(
                out_inc=out_includes,
                err_str='',
            ))

    def test_help_with_h(self):
        out, err = self.run_tuskar('help -h')
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
            [out, err],
            CommandOutput(
                out_inc=out_includes,
                out_exc=out_excludes,
                err_str='',
            ))

    def test_help_with_help(self):
        out, err = self.run_tuskar('help --help')
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
            [out, err],
            CommandOutput(
                out_inc=out_includes,
                out_exc=out_excludes,
                err_str='',
            ))

    def test_help_with_bad_argument(self):
        out, err = self.run_tuskar('help -r')
        print(err)
        err_includes = [
            'error: unrecognized arguments: -r',
        ]
        self.assertThat(
            [out, err],
            CommandOutput(
                out_str='',
                err_inc=err_includes,
            ))
