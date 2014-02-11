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
from tuskarclient.v1 import overclouds


class OvercloudManagerTest(tutils.TestCase):

    def setUp(self):
        """Create a mock API object and bind to the OvercloudManager manager.
        """
        super(OvercloudManagerTest, self).setUp()
        self.client = mock.Mock()
        self.om = overclouds.OvercloudManager(self.client)

    def test_build_url_prefix(self):
        """Test correct version prefixing of urls."""
        self.assertEqual(self.om.build_url('/base_url', overcloud_id='42'),
                         '/v1/base_url/overclouds/42')
