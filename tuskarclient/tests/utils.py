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

import copy
import fixtures
import os

from six import StringIO
import testtools

from tuskarclient.common import http


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
