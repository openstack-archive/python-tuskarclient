# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock

import tuskarclient.tests.utils as tutils
from tuskarclient.v1 import nodes


class NodeManagerTest(tutils.TestCase):
    def setUp(self):
        super(NodeManagerTest, self).setUp()
        self.api = mock.Mock()
        self.nm = nodes.NodeManager(self.api)

    def test_get(self):
        self.nm._get = mock.Mock(return_value='fake_node')

        self.assertEqual(self.nm.get(42), 'fake_node')
        self.nm._get.assert_called_with('/v1/nodes/42')

    def test_list(self):
        self.nm._list = mock.Mock(return_value=['fake_node'])

        self.assertEqual(self.nm.list(), ['fake_node'])
        self.nm._list.assert_called_with('/v1/nodes')
