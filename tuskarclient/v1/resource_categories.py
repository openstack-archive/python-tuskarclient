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
    pass


class ResourceCategoryManager(base.Manager):
    resource_class = ResourceCategory

    @staticmethod
    def _path(resource_category_id=None):

        if resource_category_id:
            return '/v1/resource_category/%s' % resource_category_id

        return '/v1/resource_category'

    def list(self):
        return self._list(self._path())

    def get(self, resource_category_id):
        return self._get(self._single_path(resource_category_id))

    def create(self, **kwargs):
        return self._create(self._path(), kwargs)

    def update(self, resource_category_id, **kwargs):
        return self._update(self._single_path(resource_category_id), kwargs)

    def delete(self, resource_category_id):
        return self._delete(self._single_path(resource_category_id))
