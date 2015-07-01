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


def _create_mock(**kwargs):
    mock_plan = mock.Mock()
    mock_plan.configure_mock(**kwargs)
    mock_plan.to_dict.return_value = kwargs
    return mock_plan

UUID_A = 'aaaaaaaa-aaaaaaaa-aaaaaaaa-aaaaaaaa'
UUID_B = 'bbbbbbbb-bbbbbbbb-bbbbbbbb-bbbbbbbb'
UUID_C = 'cccccccc-cccccccc-cccccccc-cccccccc'
UUID_D = 'dddddddd-dddddddd-dddddddd-dddddddd'


mock_roles = [
    _create_mock(uuid=UUID_A, name="Role1", version=1,
                 description="Role 1"),
    _create_mock(uuid=UUID_B, name="Role2", version=2,
                 description="Role 2"),
]

mock_plans = [
    _create_mock(uuid=UUID_C, name="Plan1", description="Plan 1",
                 roles=mock_roles),
    _create_mock(uuid=UUID_D, name="Plan2", description="Plan 2",
                 roles=[]),
]


class TestManagement(utils.TestCommand):

    def setUp(self):
        super(TestManagement, self).setUp()

        self.app.client_manager.management = mock.Mock()
