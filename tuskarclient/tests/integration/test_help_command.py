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

import tuskarclient.tests.utils as tutils


class HelpCommandTest(tutils.CommandTestCase):
    def test_help(self):
        out, err = self.run_tuskar('help')
        out_parts = [
            'usage:',
            'positional arguments:',
            'optional arguments:',
        ]
        for part in out_parts:
            self.assertIn(part, out)
        self.assertEqual(err, '')
