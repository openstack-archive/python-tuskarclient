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

from tuskarclient.v1_0 import racks
import tuskarclient.tests.utils as tutils


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
