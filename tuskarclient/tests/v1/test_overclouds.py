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
from tuskarclient.v1 import overclouds


class OvercloudsManagerTest(tutils.TestCase):

    def setUp(self):
        super(OvercloudsManagerTest, self).setUp()
        self.api = mock.Mock()
        self.om = overclouds.OvercloudsManager(self.api)

    def test_entrypoint(self):
        self.api.json_request = mock.Mock(
            return_value=('headers', {'some': 'data'}))

        self.assertEqual({'some': 'data'}, self.om.entrypoint('stack_name'))
        self.api.json_request.assert_called_with(
            'GET', '/v1/overclouds/stack_name/entrypoint')
