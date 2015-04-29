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

import logging

from cliff import lister


class ListRoles(lister.Lister):
    """List Roles."""

    log = logging.getLogger(__name__ + '.ListRoles')

    def get_parser(self, prog_name):
        parser = super(ListRoles, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.management

        roles = client.roles.list()

        return (
            ('uuid', 'name', 'version', 'description'),
            ((r.uuid, r.name, r.version, r.description)
                for r in roles)
        )
