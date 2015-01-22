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
from tuskarclient.v2 import roles


class Plan(base.Resource):
    """Represents an instance of a Plan in the Tuskar API.

    :param manager: Manager object
    :param info: dictionary representing resource attributes
    :param loaded: prevent lazy-loading if set to True
    """

    def __init__(self, manager, info, loaded=False):
        super(Plan, self).__init__(manager, info, loaded=loaded)
        self.roles = [roles.Role(None, role) for role in self.roles]


class Templates(base.Resource):
    """Represents sets of templates of a Plan in the Tuskar API.

    :param manager: Manager object
    :param info: dictionary representing resource attributes
    :param loaded: prevent lazy-loading if set to True
    """


class PlanManager(base.BaseManager):
    """PlanManager interacts with the Tuskar API and provides CRUD
    operations for the Plan type.
    """

    #: The class used to represent an Plan instance
    resource_class = Plan

    @staticmethod
    def _path(plan_id=None):

        if plan_id:
            return '/v2/plans/%s' % plan_id

        return '/v2/plans'

    def _roles_path(self, plan_id, role_id=None):
        roles_path = '%s/roles' % self._path(plan_id)

        if role_id:
            return '%(roles_path)s/%(role_id)s' % {'roles_path': roles_path,
                                                   'role_id': role_id}

        return roles_path

    def _templates_path(self, plan_id):
        templates_path = '%s/templates' % self._path(plan_id)

        return templates_path

    def get(self, plan_uuid):
        """Get the Plan by its UUID.

        :param plan_uuid: UUID of the Plan.
        :type plan_uuid: string

        :return: A Plan instance or None if its not found.
        :rtype: tuskarclient.v2.plans.Plan or None
        """
        return self._get(self._path(plan_uuid))

    def list(self):
        """Get a list of the existing Plans

        :return: A list of plans or an empty list if none are found.
        :rtype: [tuskarclient.v2.plans.Plan] or []
        """
        return self._list(self._path())

    def create(self, **fields):
        """Create a new Plan.

        :param fields: A set of key/value pairs representing a Plan.
        :type fields: string

        :return: A Plan instance or None if its not found.
        :rtype: tuskarclient.v2.plans.Plan
        """
        return self._create(self._path(), fields)

    def patch(self, plan_uuid, attribute_list):
        """Patch an existing Plan.

        :param plan_uuid: UUID of the Plan.
        :type plan_uuid: string

        :param attribute_list: a list of attribute name/value dicts
             Example: [{'name': <attr_name>, 'value': <attr_value>}]
        :type attribute_list: list

        :return: A Plan instance or None if its not found.
        :rtype: tuskarclient.v2.plans.Plan or None
        """
        return self._patch(self._path(plan_uuid),
                           attribute_list)

    def delete(self, plan_uuid):
        """Delete a Plan.

        :param plan_uuid: uuid of the Plan.
        :type plan_uuid: string

        :return: None
        :rtype: None
        """
        return self._delete(self._path(plan_uuid))

    def add_role(self, plan_uuid, role_uuid):
        """Adds a Role to a Plan.

        :param plan_uuid: UUID of the Plan.
        :type plan_uuid: string

        :param role_uuid: UUID of the Role.
        :type role_uuid: string

        :return: A Plan instance or None if its not found.
        :rtype: tuskarclient.v2.plans.Plan
        """
        return self._create(self._roles_path(plan_uuid), {'uuid': role_uuid})

    def remove_role(self, plan_uuid, role_uuid):
        """Removes a Role from a Plan.

        :param plan_uuid: UUID of the Plan.
        :type plan_uuid: string

        :param role_uuid: UUID of the Role.
        :type role_uuid: string

        :return: A Plan instance or None if its not found.
        :rtype: tuskarclient.v2.plans.Plan
        """

        rep, body = self._delete(self._roles_path(plan_uuid, role_uuid))

        return self.resource_class(self, body)

    def templates(self, plan_uuid):
        """Gets template files from a Plan.

        :param plan_uuid: UUID of the Plan.
        :type plan_uuid: string

        :return: Template files contents
        :rtype: dict
        """

        return self._get(self._templates_path(plan_uuid),
                         obj_class=Templates).to_dict()
