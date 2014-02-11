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

from tuskarclient.openstack.common.apiclient import base


class OvercloudRole(base.Resource):
    """Represents an instance of an Overcloud Role in the Tuskar API.

    :param manager: Manager object
    :param info: dictionary representing the resource attributes
    :param loaded: prevent lazy-loading if set to True
    """


class OvercloudRoleManager(base.CrudManager):
    """OvercloudRoleManager interacts with the Tuskar API and provides CRUD
    operations for the overcloud role type.

    """

    #: The class used to represent an overcloud role instance
    resource_class = OvercloudRole
    collection_key = 'overcloud_roles'
    key = 'overcloud_role'
    version_prefix = '/v1'

    def build_url(self, base_url=None, **kwargs):
        return self.version_prefix \
            + super(OvercloudRoleManager, self).build_url(base_url, **kwargs)
