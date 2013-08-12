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
from tuskarclient.v1 import data_centers


class DataCenterManagerTest(tutils.TestCase):

    def setUp(self):
        super(DataCenterManagerTest, self).setUp()
        self.api = mock.Mock()
        self.dcm = data_centers.DataCenterManager(self.api)

    def test_provision_all(self):
        self.api.json_request = mock.Mock(return_value={'some': 'data'})

        self.assertEqual({'some': 'data'}, self.dcm.provision_all())
        # FIXME: Tuskar currently requires trailing slash on this URL
        self.api.json_request.assert_called_with(
            'POST', '/v1/data_centers/')
