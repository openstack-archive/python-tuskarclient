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

from tuskarclient.common import base


class Flavor(base.Resource):

    def __repr__(self):
        return "<Flavor {0}>".format(self._info)


class FlavorManager(base.Manager):

    resource_class = Flavor

    @staticmethod
    def _path(resource_class_id, flavor_id=None):
        if flavor_id:
            return ('/v1/resource_classes/{0}/flavors/{1}'
                    .format(resource_class_id, flavor_id))
        else:
            return '/v1/resource_classes/{0}/flavors'.format(resource_class_id)

    def _single_path(self, resource_class_id, flavor_id):
        if not flavor_id:
            raise ValueError("{0} flavor_id must not be null."
                             .format(self.resource_class))
        return self._path(resource_class_id, flavor_id)

    def get(self, resource_class_id, flavor_id):
        return self._get(self._single_path(resource_class_id, flavor_id))

    def list(self, resource_class_id):
        return self._list(self._path(resource_class_id))

    def create(self, resource_class_id, **kwargs):
        return self._create(self._path(resource_class_id), kwargs)

    def update(self, resource_class_id, flavor_id, **kwargs):
        return self._update(self._single_path(resource_class_id, flavor_id),
                            kwargs)

    def delete(self, resource_class_id, flavor_id):
        return self._delete(self._single_path(resource_class_id, flavor_id))
