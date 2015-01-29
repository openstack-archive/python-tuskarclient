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
import six

import tuskarclient.tests.utils as tutils
from tuskarclient.v2 import roles_shell


def empty_args():
    args = mock.Mock(spec=[])
    for attr in ['uuid', 'name', 'version', 'description']:
        setattr(args, attr, None)
    return args


class BaseRolesShellTest(tutils.TestCase):

    def setUp(self):
        super(BaseRolesShellTest, self).setUp()
        self.outfile = six.StringIO()
        self.tuskar = mock.MagicMock()
        self.shell = roles_shell


class RolesShellTest(BaseRolesShellTest):

    @mock.patch('tuskarclient.common.formatting.print_list')
    def test_role_list(self, mock_print_list):
        args = empty_args()

        self.shell.do_role_list(self.tuskar, args, outfile=self.outfile)
        # testing the other arguments would be just copy-paste
        mock_print_list.assert_called_with(
            self.tuskar.roles.list.return_value, mock.ANY, mock.ANY,
            outfile=self.outfile
        )
