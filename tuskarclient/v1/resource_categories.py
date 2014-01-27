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


class ResourceCategory(base.Resource):
    """Represents an instance of a Resource Category in the Tuskar API.

    :param manager: Manager object
    :param info: dictionary representing resource attributes
    :param loaded: prevent lazy-loading if set to True
    """


class ResourceCategoryManager(base.Manager):
    """ResourceCategoryManager interacts with the Tuskar API and provides CRUD
    operations for the resource category type.

    """

    #: The class used to represent an resource category instance
    resource_class = ResourceCategory

    @staticmethod
    def _path(resource_category_id=None):

        if resource_category_id:
            return '/v1/resource_categories/%s' % resource_category_id

        return '/v1/resource_categories'

    def list(self):
        """Get a list of the existing resource categories

        :return: A list of resource categories or an empty list if none exist.
        :rtype: [tuskarclient.v1.resource_categories.ResourceCategory] or []
        """
        return self._list(self._path())

    def get(self, resource_category_id):
        """Get the Resource Category by its ID.

        :param id: id of the Resource Category.
        :type id: string

        :return: A Resource Category instance or None if its not found.
        :rtype: tuskarclient.v1.resource_categories.ResourceCategory or None
        """
        return self._get(self._single_path(resource_category_id))

    def create(self, **fields):
        """Create a new Resource Category.

        :param fields: A set of key/value pairs representing a ResourceCategory
        :type fields: string

        :return: A Resource Category instance or None if its not found.
        :rtype: tuskarclient.v1.resource_categories.ResourceCategory
        """
        return self._create(self._path(), fields)

    def update(self, resource_category_id, **fields):
        """Update an existing Resource Category.

        :param resource_category_id: id of the Resource Category.
        :type resource_category_id: string

        :param fields: A set of key/value pairs representing a ResourceCategory
        :type fields: string

        :return: An ResourceCategory instance or None if its not found.
        :rtype: tuskarclient.v1.resource_categories.ResourceCategory or None
        """
        return self._update(self._single_path(resource_category_id), fields)

    def delete(self, resource_category_id):
        """Delete a Resource Category.

        :param id: id of the Resource Category.
        :type id: string

        :return: None
        :rtype: None
        """
        return self._delete(self._single_path(resource_category_id))
