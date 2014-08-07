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
from tuskarclient.v2 import plans


class PlanManagerTest(tutils.TestCase):

    def setUp(self):
        """Create a mock API object and bind to the PlanManager manager.
        """
        super(PlanManagerTest, self).setUp()
        self.api = mock.Mock()
        self.pm = plans.PlanManager(self.api)

    def test_get(self):
        """Test a standard GET operation to read/retrieve the plan."""
        self.pm._get = mock.Mock(return_value='fake_plan')

        self.assertEqual(self.pm.get('fake_plan'), 'fake_plan')
        self.pm._get.assert_called_with('/v2/plans/fake_plan')

    def test_get_404(self):
        """Test a 404 response to a standard GET."""
        self.pm._get = mock.Mock(return_value=None)

        self.assertEqual(self.pm.get('fake_plan'), None)
        self.pm._get.assert_called_with('/v2/plans/fake_plan')

    def test_list(self):
        """Test retrieving a list of plans via GET."""
        self.pm._list = mock.Mock(return_value=['fake_plan'])

        self.assertEqual(self.pm.list(), ['fake_plan'])
        self.pm._list.assert_called_with('/v2/plans')

    def test_create(self):
        """Test creating a new plan via POST."""
        self.pm._create = mock.Mock(return_value=['fake_plan'])

        self.assertEqual(
            self.pm.create(dummy='dummy plan data'),
            ['fake_plan'])

        self.pm._create.assert_called_with(
            '/v2/plans',
            {'dummy': 'dummy plan data'})
