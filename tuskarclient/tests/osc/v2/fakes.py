#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import mock
from openstackclient.tests import utils


mock_roles = [
    mock.Mock(uuid="UUID1", version=1, description="Mock Role 1"),
    mock.Mock(uuid="UUID2", version=2, description="Mock Role 2"),
]
mock_roles[0].configure_mock(name="Role 1 Name")
mock_roles[1].configure_mock(name="Role 2 Name")

mock_plans = [
    mock.Mock(uuid="UUID1", description="Plan 1",
              roles=mock_roles),
    mock.Mock(uuid="UUID2", description="Plan 2", roles=[]),
]
mock_plans[0].configure_mock(name="Plan 1 Name")
mock_plans[1].configure_mock(name="Plan 2 Name")


class TestManagement(utils.TestCommand):

    def setUp(self):
        super(TestManagement, self).setUp()

        self.app.client_manager.management = mock.Mock()
