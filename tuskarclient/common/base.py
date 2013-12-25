# Copyright 2012 OpenStack LLC.
# All Rights Reserved.
#
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

"""
Base utilities to build API operation managers and objects on top of.
"""

import copy

from tuskarclient.openstack.common.apiclient import base


class TuskarManager(base.CrudManager):
    """Managers interact with a particular type of API
    (samples, meters, alarms, etc.) and provide CRUD operations for them.
    """

    @staticmethod
    def _path(id=None):
        """Helper method to be defined in subclasses. It returns the
        resource/collection path. If id is given, then single resource
        path is returned. Otherwise the collection path is returned.

        :param id: id of the resource (optional)
        """
        raise NotImplementedError("_path method not implemented.")

    def _single_path(self, id):
        """This is like the _path method, but it asserts that the rack_id
        parameter is not None. This is useful e.g. when you want to make sure
        that you can't issue a DELETE request on a collection URL.
        """
        if not id:
            raise ValueError("{0} id for deletion must not be null."
                             .format(self.resource_class))
        return self._path(id)

    def _create(self, url, body):
        return self._post(url, body)

    def _get(self, url, **kwargs):
        kwargs.setdefault('expect_single', True)
        try:
            return self._list(url, **kwargs)[0]
        except IndexError:
            return None


class Resource(base.Resource):
    """A resource represents a particular instance of an object (tenant, user,
    etc). This is pretty much just a bag for attributes.

    :param manager: Manager object
    :param info: dictionary representing resource attributes
    :param loaded: prevent lazy-loading if set to True
    """

    def to_dict(self):
        return copy.deepcopy(self._info)
