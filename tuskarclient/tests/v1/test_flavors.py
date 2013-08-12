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
from tuskarclient.v1 import flavors


class FlavorManagerTest(tutils.TestCase):

    def setUp(self):
        super(FlavorManagerTest, self).setUp()
        self.api = mock.Mock()
        self.fm = flavors.FlavorManager(self.api)

    def test_get(self):
        self.fm._get = mock.Mock(return_value='fake_flavor')

        self.assertEqual('fake_flavor', self.fm.get(5, 42))
        self.fm._get.assert_called_with('/v1/resource_classes/5/flavors/42')

    def test_list(self):
        self.fm._list = mock.Mock(return_value=['fake_flavor'])

        self.assertEqual(['fake_flavor'], self.fm.list(5))
        self.fm._list.assert_called_with('/v1/resource_classes/5/flavors')

    def test_create(self):
        self.fm._create = mock.Mock(return_value=['fake_flavor'])

        self.assertEqual(
            ['fake_flavor'],
            self.fm.create(5, dummy='dummy flavor data'))

        self.fm._create.assert_called_with(
            '/v1/resource_classes/5/flavors',
            {'dummy': 'dummy flavor data'})

    def test_update(self):
        self.fm._update = mock.Mock(return_value=['fake_flavor'])

        self.assertEqual(
            ['fake_flavor'],
            self.fm.update(5, 42, dummy='dummy flavor data'))

        self.fm._update.assert_called_with(
            '/v1/resource_classes/5/flavors/42',
            {'dummy': 'dummy flavor data'})

    def test_delete(self):
        self.fm._delete = mock.Mock(return_value=None)

        self.assertEqual(None, self.fm.delete(5, 42))
        self.fm._delete.assert_called_with('/v1/resource_classes/5/flavors/42')
