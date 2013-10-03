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

from tuskarclient.tests import utils as tutils
from tuskarclient.v1 import client


class ClientTest(tutils.TestCase):

    def setUp(self):
        super(ClientTest, self).setUp()
        self.endpoint = "http://fakeurl:1234"
        self.client = client.Client(self.endpoint)

    def test_managers_present(self):
        self.assertEqual("RackManager",
                         self.client.racks.__class__.__name__)
        self.assertEqual(self.client, self.client.racks.api)

        self.assertEqual("ResourceClassManager",
                         self.client.resource_classes.__class__.__name__)
        self.assertEqual(self.client, self.client.resource_classes.api)

        self.assertEqual("NodeManager",
                         self.client.nodes.__class__.__name__)
        self.assertEqual(self.client, self.client.nodes.api)

        self.assertEqual("FlavorManager",
                         self.client.flavors.__class__.__name__)
        self.assertEqual(self.client, self.client.flavors.api)

        self.assertEqual("DataCenterManager",
                         self.client.data_centers.__class__.__name__)
        self.assertEqual(self.client, self.client.data_centers.api)
