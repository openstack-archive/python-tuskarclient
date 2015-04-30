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

from cliff import command
from cliff import lister
from cliff import show


class CreateManagementPlan(show.ShowOne):
    """Create a Management Plan."""

    log = logging.getLogger(__name__ + '.CreateManagementPlan')

    def get_parser(self, prog_name):
        parser = super(CreateManagementPlan, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)


class DeleteManagementPlan(command.Command):
    """Delete a Management Plan."""

    log = logging.getLogger(__name__ + '.DeleteManagementPlan')

    def get_parser(self, prog_name):
        parser = super(DeleteManagementPlan, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)


class ListManagementPlans(lister.Lister):
    """List the Management Plans."""

    log = logging.getLogger(__name__ + '.ListManagementPlans')

    def get_parser(self, prog_name):
        parser = super(ListManagementPlans, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.management

        plans = client.plans.list()

        return (
            ('uuid', 'name', 'description', 'roles'),
            ((p.uuid, p.name, p.description,
                ', '.join(r.name for r in p.roles))
                for p in plans)
        )


class SetManagementPlan(show.ShowOne):
    """Update a Management Plans properties."""

    log = logging.getLogger(__name__ + '.SetManagementPlan')

    def get_parser(self, prog_name):
        parser = super(SetManagementPlan, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)


class ShowManagementPlan(show.ShowOne):
    """Show a Management Plan."""

    log = logging.getLogger(__name__ + '.ShowManagementPlan')

    def get_parser(self, prog_name):
        parser = super(ShowManagementPlan, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)


class AddManagementPlanRole(show.ShowOne):
    """Add a Role to a Management Plan."""

    log = logging.getLogger(__name__ + '.AddManagementPlanRole')

    def get_parser(self, prog_name):
        parser = super(AddManagementPlanRole, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)


class RemoveManagementPlanRole(show.ShowOne):
    """Remove a Role from a Management Plan."""

    log = logging.getLogger(__name__ + '.RemoveManagementPlanRole')

    def get_parser(self, prog_name):
        parser = super(RemoveManagementPlanRole, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)


class DownloadManagementPlan(command.Command):
    """Download the a Management Plan."""

    log = logging.getLogger(__name__ + '.DownloadManagementPlan')

    def get_parser(self, prog_name):
        parser = super(DownloadManagementPlan, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
