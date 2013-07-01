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
Command-line interface to the Heat API.
"""

from __future__ import print_function

import logging
import logging.handlers
import sys

logger = logging.getLogger(__name__)


class TuskarShell(object):

    def __init__(self, args):
        self.args = args

    def run(self):
        pass


def main():
    logger.addHandler(logging.StreamHandler(sys.stderr))
    try:
        TuskarShell(sys.argv[1:]).run()
    except Exception as e:
        logger.exception("Exiting due to an error:")
        sys.exit(1)

if __name__ == '__main__':
    main()
