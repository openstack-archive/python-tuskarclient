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
                 err_str=None, err_inc=[], err_exc=[],
                 return_code=None):
        self.out_str = out_str
        self.out_inc = out_inc
        self.out_exc = out_exc
        self.err_str = err_str
        self.err_inc = err_inc
        self.err_exc = err_exc
        self.return_code = return_code

    def match(self, outputs):
        out, err, ret = outputs[0], outputs[1], outputs[2]
        errors = []

        # tests for exact output and error output match
        errors.append(self.match_output(out, self.out_str, type='output'))
        errors.append(self.match_output(err, self.err_str, type='error'))

        # tests for what output should include and what it should not
        errors.append(self.match_includes(out, self.out_inc, type='output'))
        errors.append(self.match_excludes(out, self.out_exc, type='output'))

        # tests for what error output should include and what it should not
        errors.append(self.match_includes(err, self.err_inc, type='error'))
        errors.append(self.match_excludes(err, self.err_exc, type='error'))

        # test for return code
        errors.append(self.match_return_code(ret, self.return_code))

        # get first non None item or None if none is found and return it
        return next((item for item in errors if item is not None), None)

    def match_return_code(self, return_code, expected_return_code):
        if expected_return_code is not None:
            if expected_return_code != return_code:
                return CommandOutputReturnCodeMismatch(
                    return_code, expected_return_code)

    def match_output(self, output, expected_output, type='output'):
        if expected_output is not None:
            if expected_output != output:
                return CommandOutputMismatch(
                    output, expected_output, type=type)

    def match_includes(self, output, includes, type='output'):
        for part in includes:
            if part not in output:
                return CommandOutputMissingMismatch(output, part, type=type)

    def match_excludes(self, output, excludes, type='error'):
        for part in excludes:
            if part in output:
                return CommandOutputExtraMismatch(output, part, type=type)


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


class CommandOutputReturnCodeMismatch(object):
    def __init__(self, ret, ret_exp):
        self.ret = ret
        self.ret_exp = ret_exp

    def describe(self):
        return "Return code is '%s' but expected '%s'"\
            % (self.ret, self.ret_exp)

    def get_details(self):
        return {}


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
            CommandOutput(
                out_inc=out_includes,
                err_str='',
                return_code=0,
            ))

    def test_help_with_h(self):
        results = self.run_tuskar('help -h')
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
            CommandOutput(
                out_inc=out_includes,
                out_exc=out_excludes,
                err_str='',
                return_code=0,
            ))

    def test_help_with_help(self):
        results = self.run_tuskar('help --help')
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
            CommandOutput(
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
            CommandOutput(
                out_str='',
                err_inc=err_includes,
                return_code=2,
            ))
