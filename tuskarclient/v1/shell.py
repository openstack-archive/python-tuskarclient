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

from tuskarclient.common import utils
from tuskarclient.v1 import data_centers_shell
from tuskarclient.v1 import flavors_shell
from tuskarclient.v1 import nodes_shell
from tuskarclient.v1 import racks_shell
from tuskarclient.v1 import resource_classes_shell

COMMAND_MODULES = [
    data_centers_shell,
    flavors_shell,
    nodes_shell,
    racks_shell,
    resource_classes_shell,
]


def enhance_parser(parser, subparsers):
    '''Take a basic (nonversioned) parser and enhance it with
    commands and options specific for this version of API.

    :param parser: top level parser :param subparsers: top level
        parser's subparsers collection where subcommands will go
    '''
    for command_module in COMMAND_MODULES:
        utils.define_commands_from_module(subparsers, command_module)
