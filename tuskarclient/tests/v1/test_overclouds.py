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

import mock

import tuskarclient.tests.utils as tutils
from tuskarclient.v1 import overclouds


class OvercloudManagerTest(tutils.TestCase):

    def setUp(self):
        """Create a mock API object and bind to the OvercloudManager manager.
        """
        super(OvercloudManagerTest, self).setUp()
        self.api = mock.Mock()
        self.om = overclouds.OvercloudManager(self.api)

    def test_get(self):
        """Test a standard GET operation to read/retrieve the overcloud."""
        self.om._get = mock.Mock(return_value='fake_overcloud')

        self.assertEqual(self.om.get('fake_overcloud'), 'fake_overcloud')
        self.om._get.assert_called_with('/v1/overclouds/fake_overcloud')

    def test_get_404(self):
        """Test a 404 response to a standard GET."""
        self.om._get = mock.Mock(return_value=None)

        self.assertEqual(self.om.get('fake_overcloud'), None)
        self.om._get.assert_called_with('/v1/overclouds/fake_overcloud')

    def test_list(self):
        """Test retrieving a list of overclouds via GET."""
        self.om._list = mock.Mock(return_value=['fake_overcloud'])

        self.assertEqual(self.om.list(), ['fake_overcloud'])
        self.om._list.assert_called_with('/v1/overclouds')

    def test_create(self):
        """Test creating a new overcloud via POST."""
        self.om._create = mock.Mock(return_value=['fake_overcloud'])

        self.assertEqual(
            self.om.create(dummy='dummy overcloud data'),
            ['fake_overcloud'])

        self.om._create.assert_called_with(
            '/v1/overclouds',
            {'dummy': 'dummy overcloud data'})

    def test_update(self):
        """Test updating an overcloud via POST."""
        self.om._update = mock.Mock(return_value=['fake_overcloud'])

        self.assertEqual(
            self.om.update(42, dummy='dummy overcloud data'),
            ['fake_overcloud'])

        self.om._update.assert_called_with(
            '/v1/overclouds/42',
            {'dummy': 'dummy overcloud data'})

    def test_delete(self):
        """Test deleting/removing an overcloud via DELETE."""
        self.om._delete = mock.Mock(return_value=None)

        self.assertEqual(self.om.delete(42), None)
        self.om._delete.assert_called_with('/v1/overclouds/42')

    def test_template_parameters(self):
        """Test getting the template parameters via GET."""
        self.om._get = mock.Mock(return_value={})

        self.assertEqual(self.om.template_parameters(), {})
        self.om._get.assert_called_with('/v1/overclouds/template_parameters')
