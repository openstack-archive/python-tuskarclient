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

import mock

from tuskarclient.common import base
from tuskarclient.tests import utils as tutils


class ManagerTest(tutils.TestCase):

    def setUp(self):
        super(ManagerTest, self).setUp()
        self.api = mock.Mock()
        self.m = base.Manager(self.api)

    def test_get(self):
        self.m._list = mock.Mock(return_value=['fake_resource'])
        got = self.m._get('url', response_key='response_key',
                          obj_class='obj_class', body='body')

        self.assertEqual('fake_resource', got)
        self.m._list.assert_called_with('url', response_key='response_key',
                                        obj_class='obj_class',
                                        body='body', expect_single=True)

    def test_get_nonexistent(self):
        self.m._list = mock.Mock(return_value=[])
        got = self.m._get('url', response_key='response_key',
                          obj_class='obj_class', body='body')

        self.assertEqual(None, got)
        self.m._list.assert_called_with('url', response_key='response_key',
                                        obj_class='obj_class',
                                        body='body', expect_single=True)

    def test_path(self):
        self.assertRaises(NotImplementedError, self.m._path)

    def test_single_path(self):
        self.m._path = mock.Mock(return_value='/v1/somethings/42')
        self.m._single_path(42)
        self.m._path.assert_called_with(42)

    def test_single_path_without_id(self):
        self.assertRaises(ValueError, self.m._single_path, None)
