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

from tuskarclient.common import base
from tuskarclient.openstack.common.apiclient import base as common_base


class OvercloudRole(common_base.Resource):
    """Represents an instance of an Overcloud Role in the Tuskar API.

    :param manager: Manager object
    :param info: dictionary representing the resource attributes
    :param loaded: prevent lazy-loading if set to True
    """


class OvercloudRoleManager(base.Manager):
    """OvercloudRoleManager interacts with the Tuskar API and provides CRUD
    operations for the overcloud role type.
    """

    #: The class used to represent an overcloud role instance
    resource_class = OvercloudRole

    @staticmethod
    def _path(overcloud_role_id=None):

        if overcloud_role_id:
            return '/v1/overcloud_roles/%s' % overcloud_role_id

        return '/v1/overcloud_roles'

    def list(self):
        """Get a list of the existing Overcloud Roles

        :return: A list of Overcloud Roles or an empty list if none exist.
        :rtype: [tuskarclient.v1.overcloud_roles.OvercloudRole] or []
        """
        return self._list(self._path())

    def get(self, overcloud_role_id):
        """Get the Overcloud Role by its ID.

        :param id: id of the Overcloud Role.
        :type id: string

        :return: A Overcloud Role instance or None if its not found.
        :rtype: tuskarclient.v1.overcloud_roles.OvercloudRole or None
        """
        return self._get(self._single_path(overcloud_role_id))

    def create(self, **fields):
        """Create a new Overcloud Role.

        :param fields: A set of key/value pairs representing a OvercloudRole
        :type fields: string

        :return: A Overcloud Role instance or None if its not found.
        :rtype: tuskarclient.v1.overcloud_roles.OvercloudRole
        """
        return self._create(self._path(), fields)

    def update(self, overcloud_role_id, **fields):
        """Update an existing Overcloud Role.

        :param overcloud_role_id: id of the Overcloud Role.
        :type overcloud_role_id: string

        :param fields: A set of key/value pairs representing a OvercloudRole
        :type fields: string

        :return: An OvercloudRole instance or None if its not found.
        :rtype: tuskarclient.v1.overcloud_roles.OvercloudRole or None
        """
        return self._update(self._single_path(overcloud_role_id), fields)

    def delete(self, overcloud_role_id):
        """Delete a Overcloud Role.

        :param id: id of the Overcloud Role.
        :type id: string

        :return: None
        :rtype: None
        """
        return self._delete(self._single_path(overcloud_role_id))
