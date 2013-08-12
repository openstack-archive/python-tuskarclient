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

import tuskarclient.tests.utils as tutils
from tuskarclient.v1 import racks


class RackManagerTest(tutils.TestCase):

    def setUp(self):
        super(RackManagerTest, self).setUp()
        self.api = mock.Mock()
        self.rm = racks.RackManager(self.api)

    def test_get(self):
        self.rm._get = mock.Mock(return_value='fake_rack')

        self.assertEqual(self.rm.get(42), 'fake_rack')
        self.rm._get.assert_called_with('/v1/racks/42')

    def test_list(self):
        self.rm._list = mock.Mock(return_value=['fake_rack'])

        self.assertEqual(self.rm.list(), ['fake_rack'])
        self.rm._list.assert_called_with('/v1/racks')

    def test_create(self):
        self.rm._create = mock.Mock(return_value=['fake_rack'])

        self.assertEqual(
            self.rm.create(dummy='dummy rack data'),
            ['fake_rack'])

        self.rm._create.assert_called_with(
            '/v1/racks',
            {'dummy': 'dummy rack data'})

    def test_update(self):
        self.rm._update = mock.Mock(return_value=['fake_rack'])

        self.assertEqual(
            self.rm.update(42, dummy='dummy rack data'),
            ['fake_rack'])

        self.rm._update.assert_called_with(
            '/v1/racks/42',
            {'dummy': 'dummy rack data'})

    def test_delete(self):
        self.rm._delete = mock.Mock(return_value=None)

        self.assertEqual(self.rm.delete(42), None)
        self.rm._delete.assert_called_with('/v1/racks/42')
