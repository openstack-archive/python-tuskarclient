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


class HasManager(object):

    def __init__(self, cls_name, attr_name):
        self.cls_name = cls_name
        self.attr_name = attr_name

    def match(self, client):
        if not hasattr(client, self.attr_name):
            return ManagerClassMismatch(client, self.cls_name, self.attr_name)

        obj = getattr(client, self.attr_name)
        if (client != obj.api or self.cls_name != obj.__class__.__name__):
            return ManagerClassMismatch(client, self.cls_name, self.attr_name)
        else:
            return None


class ManagerClassMismatch(object):

    def __init__(self, client, cls_name, attr_name):
        self.client = client
        self.cls_name = cls_name
        self.attr_name = attr_name

    def describe(self):
        return "Class %r mismatch for attribute %r on %r" % (
            self.cls_name, self.attr_name, self.client)

    def get_details(self):
        return {}


class ClientTest(tutils.TestCase):

    def setUp(self):
        super(ClientTest, self).setUp()
        self.endpoint = "http://fakeurl:1234"
        self.client = client.Client(self.endpoint)

    def test_managers_present(self):
        self.assertThat(self.client, HasManager('RackManager', 'racks'))
        self.assertThat(self.client, HasManager('ResourceClassManager',
                                                'resource_classes'))
        self.assertThat(self.client, HasManager('NodeManager', 'nodes'))
        self.assertThat(self.client, HasManager('FlavorManager', 'flavors'))
        self.assertThat(self.client, HasManager('DataCenterManager',
                                                'data_centers'))
        self.assertThat(self.client, HasManager('OvercloudManager',
                                                'overclouds'))
