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


class Overcloud(base.Resource):
    pass


class OvercloudManager(base.Manager):

    resource_class = Overcloud

    @staticmethod
    def _path(id=None):
        return '/v1/overcloud/%s' % id if id else '/v1/overcloud'

    def list(self):
        return self._list(self._path())

    def get(self, id):
        return self._get(self._single_path(id))

    def create(self, **kwargs):
        return self._create(self._path(), kwargs)

    def update(self, id, **kwargs):
        return self._update(self._single_path(id), kwargs)

    def delete(self, id):
        return self._delete(self._single_path(id))
