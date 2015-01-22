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


class Role(base.Resource):
    """Represents an instance of a Role in the Tuskar API.

    :param manager: Manager object
    :param info: dictionary representing resource attributes
    :param loaded: prevent lazy-loading if set to True
    """


class RoleManager(base.BaseManager):
    """RoleManager interacts with the Tuskar API and provides
    operations for adding/removing Roles to/from Plans.
    """

    # The class used to represent a Role instance
    resource_class = Role

    @staticmethod
    def _path(role_id=None):

        if role_id:
            return '/v2/roles/%s' % role_id

        return '/v2/roles'

    def list(self):
        """Get a list of the existing Roles

        :return: A list of Roles or an empty list if none are found.
        :rtype: [tuskarclient.v2.plans.Role] or []
        """
        return self._list(self._path())
