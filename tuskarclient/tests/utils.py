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

import argparse
import copy
import fixtures
from gettext import gettext as _
import os
import sys

from six import StringIO
import testtools

from tuskarclient.common import http
from tuskarclient import shell


class TestCase(testtools.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        if (os.environ.get('OS_STDOUT_CAPTURE') == 'True' or
                os.environ.get('OS_STDOUT_CAPTURE') == '1'):
            stdout = self.useFixture(fixtures.StringStream('stdout')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stdout', stdout))
        if (os.environ.get('OS_STDERR_CAPTURE') == 'True' or
                os.environ.get('OS_STDERR_CAPTURE') == '1'):
            stderr = self.useFixture(fixtures.StringStream('stderr')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stderr', stderr))


class CommandTestCase(TestCase):
    def setUp(self):
        super(CommandTestCase, self).setUp()
        self.tuskar_bin = os.path.join(
            os.path.dirname(os.path.realpath(sys.executable)),
            'tuskar')

    def run_tuskar(self, params=''):
        args = params.split()
        out = StringIO()
        err = StringIO()
        ArgumentParserForTests.OUT = out
        ArgumentParserForTests.ERR = err
        try:
            shell.TuskarShell(
                args, argument_parser_class=ArgumentParserForTests).run()
        except TestExit:
            pass
        outvalue = out.getvalue()
        errvalue = err.getvalue()
        return [outvalue, errvalue]


class CommandOutputMatches(object):
    def __init__(self,
                 out_str=None, out_inc=None, out_exc=None,
                 err_str=None, err_inc=None, err_exc=None,
                 return_code=None):
        self.out_str = out_str
        self.out_inc = out_inc or []
        self.out_exc = out_exc or []
        self.err_str = err_str
        self.err_inc = err_inc or []
        self.err_exc = err_exc or []
        self.return_code = return_code

    def match(self, outputs):
        out, err = outputs[0], outputs[1]
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


class TestExit(Exception):
    pass


class ArgumentParserForTests(argparse.ArgumentParser):
    OUT = sys.stdout
    ERR = sys.stderr

    def __init__(self, **kwargs):
        self.out = ArgumentParserForTests.OUT
        self.err = ArgumentParserForTests.ERR

        super(ArgumentParserForTests, self).__init__(**kwargs)

    def error(self, message):
        self.print_usage(self.err)
        self.exit(2, _('%(prog)s: error: %(message)s\n') %
                  {'prog': self.prog, 'message': message})

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, self.err)
        raise TestExit

    def print_usage(self, file=None):
        if file is None:
            file = self.out
        self._print_message(self.format_usage(), file)

    def print_help(self, file=None):
        if file is None:
            file = self.out
        self._print_message(self.format_help(), file)

    def print_version(self, file=None):
        import warnings
        warnings.warn(
            'The print_version method is deprecated -- the "version" '
            'argument to ArgumentParser is no longer supported.',
            DeprecationWarning)
        self._print_message(self.format_version(), file)

    def _print_message(self, message, file=None):
        if message:
            if file is None:
                file = self.err
            file.write(message)


class FakeAPI(object):
    def __init__(self, fixtures):
        self.fixtures = fixtures
        self.calls = []

    def _request(self, method, url, headers=None, body=None):
        call = (method, url, headers or {}, body)
        self.calls.append(call)
        return self.fixtures[url][method]

    def raw_request(self, *args, **kwargs):
        fixture = self._request(*args, **kwargs)
        body_iter = http.ResponseBodyIterator(
            StringIO.StringIO(fixture[1]))
        return FakeResponse(fixture[0]), body_iter

    def json_request(self, *args, **kwargs):
        fixture = self._request(*args, **kwargs)
        return FakeResponse(fixture[0]), fixture[1]


class FakeResponse(object):
    def __init__(self, headers, body=None, version=None):
        """:param headers: dict representing HTTP response headers
        :param body: file-like object
        """
        self.headers = headers
        self.body = body

    def getheaders(self):
        return copy.deepcopy(self.headers).items()

    def getheader(self, key, default):
        return self.headers.get(key, default)

    def read(self, amt):
        return self.body.read(amt)


def create_test_dictionary_pair(default_keys, redundant_keys, missing_keys,
                                **kwargs):
    """Creates a pair of dictionaries for testing

    This function creates two dictionaries from three sets of keys.

    The first returned dictionary contains keys from default_keys,
    keys from redundant_keys but is missing keys from missing_keys.
    All with value of key + '_value'.

    The second returned dictionary contains keys from default_keys
    with value of key + '_value' except for keys from missing_keys.
    These contains value None.

    These two dictionaries can be used in test cases when testing
    if tested function filters out set of keys from kwargs
    and passes it to other function.

    :param default_keys: set of keys expected to be passed on
    :param redundant_keys: set of keys expected to be filtered out
    :param missing_keys: set of keys missing from passed_dictionary
    and expected to be set to None
    :param kwargs: key translation pairs. original=new_one will create
    original='original_value' in passed_dictionary and
    new_one='original_value' in called_dictionary.
    """
    passed_dictionary = {}
    translations = kwargs

    for key in default_keys | redundant_keys:
        if key not in missing_keys:
            passed_dictionary[key] = key + '_value'

    called_dictionary = passed_dictionary.copy()

    for key in redundant_keys:
        del called_dictionary[key]

    for key in missing_keys:
        called_dictionary[key] = None

    for key in translations:
        if key in called_dictionary:
            # create new key with name from translations dict
            # with original value
            called_dictionary[translations[key]] = called_dictionary[key]
            # delete original key
            del called_dictionary[key]

    return passed_dictionary, called_dictionary
