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


class Rack(base.Resource):

    def __repr__(self):
        return "<Rack {0}>".format(self._info)


class RackManager(base.Manager):

    resource_class = Rack

    @staticmethod
    def _path(id=None):
        return '/v1/racks/%s' % id if id else '/v1/racks'

    def get(self, rack_id):
        return self._get(self._single_path(rack_id))

    def list(self):
        return self._list(self._path())

    def create(self, **kwargs):
        return self._create(self._path(), kwargs)

    def update(self, rack_id, **kwargs):
        return self._update(self._single_path(rack_id), kwargs)

    def delete(self, rack_id):
        return self._delete(self._single_path(rack_id))
