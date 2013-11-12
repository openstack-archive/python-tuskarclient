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


class Overcloud(base.Resource):

    def __repr__(self):
        return "<Overcloud {0}>".format(self._info)


class OvercloudManager(base.Manager):

    resource_class = Overcloud

    @staticmethod
    def _path(stack_name):
        return '/v1/overclouds/%s' % stack_name

    def get(self, stack_name):
        return self._get(self._single_path(stack_name))
