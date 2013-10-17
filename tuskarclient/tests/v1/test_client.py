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

    def assert_manager_present(self, cls_name, obj):
        self.assertEqual(cls_name,
                         obj.__class__.__name__)
        self.assertEqual(self.client, obj.api)

    def test_managers_present(self):
        self.assert_manager_present("RackManager", self.client.racks)
        self.assert_manager_present("ResourceClassManager",
                                    self.client.resource_classes)
        self.assert_manager_present("NodeManager", self.client.nodes)
        self.assert_manager_present("FlavorManager", self.client.flavors)
        self.assert_manager_present("DataCenterManager",
                                    self.client.data_centers)
        self.assert_manager_present("OvercloudsManager",
                                    self.client.overclouds)
