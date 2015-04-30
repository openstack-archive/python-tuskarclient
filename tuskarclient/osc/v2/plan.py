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

from __future__ import print_function

import logging
import sys

from cliff import command
from cliff import lister
from cliff import show

from tuskarclient.common import utils


class CreateManagementPlan(show.ShowOne):
    """Create a Management Plan."""

    log = logging.getLogger(__name__ + '.CreateManagementPlan')

    def get_parser(self, prog_name):
        parser = super(CreateManagementPlan, self).get_parser(prog_name)

        parser.add_argument(
            'name',
            help="Name of the plan being created."
        )

        parser.add_argument(
            '-d', '--description',
            help='A textual description of the plan.')

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.management

        plan = client.plans.create(
            name=parsed_args.name,
            description=parsed_args.description
        )

        return self.dict2columns(plan.to_dict())


class DeleteManagementPlan(command.Command):
    """Delete a Management Plan."""

    log = logging.getLogger(__name__ + '.DeleteManagementPlan')

    def get_parser(self, prog_name):
        parser = super(DeleteManagementPlan, self).get_parser(prog_name)

        parser.add_argument(
            'plan_uuid',
            help="The UUID of the plan being deleted."
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.management

        client.plans.delete(parsed_args.plan_uuid)


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

        parser.add_argument(
            'plan_uuid',
            help="The UUID of the plan being updated."
        )

        parser.add_argument(
            '-P', '--parameter', dest='parameters', metavar='<KEY1=VALUE1>',
            help=('Set a parameter in the Plan. This can be specified '
                  'multiple times.'),
            action='append'
        )

        parser.add_argument(
            '-F', '--flavor', dest='flavors', metavar='<ROLE=FLAVOR>',
            help=('Set the flavor for a role in the Plan. This can be '
                  'specified multiple times.'),
            action='append'
        )

        parser.add_argument(
            '-S', '--scale', dest='scales', metavar='<ROLE=SCALE-COUNT>',
            help=('Set the Scale count for a role in the Plan. This can be '
                  'specified multiple times.'),
            action='append'
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.management

        plan = client.plans.get(parsed_args.plan_uuid)
        roles = plan.roles

        patch = []

        patch.extend(utils.parameters_args_to_patch(parsed_args.parameters))
        patch.extend(utils.args_to_patch(parsed_args.flavors, roles, "Flavor"))
        patch.extend(utils.args_to_patch(parsed_args.scales, roles, "count"))

        if len(patch) > 0:
            plan = client.plans.patch(parsed_args.plan_uuid, patch)
        else:
            print(("WARNING: No valid arguments passed. No update operation "
                   "has been performed."), file=sys.stderr)

        return self.dict2columns(plan.to_dict())


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
