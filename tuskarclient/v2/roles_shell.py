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

from __future__ import print_function

import sys

import tuskarclient.common.formatting as fmt


def do_role_list(tuskar, args, outfile=sys.stdout):
    """Show a list of the Roles."""
    roles = tuskar.roles.list()
    fields = ['uuid', 'name', 'version', 'description']

    formatters = {
    }

    fmt.print_list(roles, fields, formatters, outfile=outfile)
