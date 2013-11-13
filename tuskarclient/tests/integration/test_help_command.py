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

import os
import subprocess
import sys

import tuskarclient.tests.utils as tutils


class HelpCommandTest(tutils.TestCase):
    def setUp(self):
        super(HelpCommandTest, self).setUp()
        self.tuskar_bin = os.path.join(
            os.path.dirname(os.path.realpath(sys.executable)),
            'tuskar')

    def test_help(self):
        command = subprocess.Popen(
            [self.tuskar_bin, 'help'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = command.communicate()
        out_parts = [
            'usage:',
            'positional arguments:',
            'optional arguments:',
        ]
        for part in out_parts:
            self.assertIn(part, out)
        self.assertEqual(err, '')
