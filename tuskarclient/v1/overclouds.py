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


class Overcloud(common_base.Resource):
    """Represents an instance of a Overcloud in the Tuskar API.

    :param manager: Manager object
    :param info: dictionary representing resource attributes
    :param loaded: prevent lazy-loading if set to True
    """


class OvercloudManager(base.Manager):
    """OvercloudManager interacts with the Tuskar API and provides CRUD
    operations for the Overcloud type.
    """

    #: The class used to represent an Overcloud instance
    resource_class = Overcloud

    @staticmethod
    def _path(overcloud_id=None):

        if overcloud_id:
            return '/v1/overclouds/%s' % overcloud_id

        return '/v1/overclouds'

    def list(self):
        """Get a list of the existing Overclouds

        :return: A list of overclounds or an empty list if none are found.
        :rtype: [tuskarclient.v1.overclouds.Overcloud] or []
        """
        return self._list(self._path())

    def get(self, overcloud_id):
        """Get the Overcloud by its ID.

        :param overcloud_id: id of the Overcloud.
        :type overcloud_id: string

        :return: A Overcloud instance or None if its not found.
        :rtype: tuskarclient.v1.overclouds.Overcloud or None
        """
        return self._get(self._single_path(overcloud_id))

    def create(self, **fields):
        """Create a new Overcloud.

        :param fields: A set of key/value pairs representing a Overcloud.
        :type fields: string

        :return: A Overcloud instance or None if its not found.
        :rtype: tuskarclient.v1.overclouds.Overcloud
        """
        return self._create(self._path(), fields)

    def update(self, overcloud_id, **fields):
        """Update an existing Overcloud.

        :param overcloud_id: id of the Overcloud.
        :type overcloud_id: string

        :param fields: A set of key/value pairs representing the Overcloud.
        :type fields: string

        :return: A Overcloud instance or None if its not found.
        :rtype: tuskarclient.v1.overclouds.Overcloud or None
        """
        return self._update(self._single_path(overcloud_id), fields)

    def delete(self, overcloud_id):
        """Delete an Overcloud.

        :param overcloud_id: id of the Overcloud.
        :type overcloud_id: string

        :return: None
        :rtype: None
        """
        return self._delete(self._single_path(overcloud_id))

    def template_parameters(self):
        """Get the template parameters from the Tuskar API.

        :return: Dictionary containing template parameters
        :rtype: dict
        """
        return self._get("{0}/template_parameters".format(self._path()))
