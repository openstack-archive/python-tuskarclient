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
from tuskarclient.v1 import resource_classes


class ResourceClassManagerTest(tutils.TestCase):
    def setUp(self):
        super(ResourceClassManagerTest, self).setUp()
        self.api = mock.Mock()
        self.rcm = resource_classes.ResourceClassManager(self.api)

    def test_get(self):
        self.rcm._get = mock.Mock(return_value='fake_resource_class')

        self.assertEqual(self.rcm.get(42), 'fake_resource_class')
        self.rcm._get.assert_called_with('/v1/resource_classes/42')

    def test_list(self):
        self.rcm._list = mock.Mock(return_value=['fake_resource_class'])

        self.assertEqual(self.rcm.list(), ['fake_resource_class'])
        self.rcm._list.assert_called_with('/v1/resource_classes')

    def test_create(self):
        self.rcm._create = mock.Mock(return_value=['fake_resource_class'])

        self.assertEqual(
            self.rcm.create(dummy='dummy resource class data'),
            ['fake_resource_class'])

        self.rcm._create.assert_called_with(
            '/v1/resource_classes',
            {'dummy': 'dummy resource class data'})

    def test_update(self):
        self.rcm._update = mock.Mock(return_value=['fake_resource_class'])

        self.assertEqual(
            self.rcm.update(42, dummy='dummy resource class data'),
            ['fake_resource_class'])

        self.rcm._update.assert_called_with(
            '/v1/resource_classes/42',
            {'dummy': 'dummy resource class data'})

    def test_delete(self):
        self.rcm._delete = mock.Mock(return_value=None)

        self.assertEqual(self.rcm.delete(42), None)
        self.rcm._delete.assert_called_with('/v1/resource_classes/42')
