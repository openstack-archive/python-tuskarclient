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

import os
import sys

import tuskarclient.common.formatting as fmt
from tuskarclient.common import utils


def do_plan_list(tuskar, args, outfile=sys.stdout):
    """Show a list of the Plans."""
    plans = tuskar.plans.list()
    fields = ['uuid', 'name', 'description', 'roles']

    formatters = {
        'roles': fmt.list_plan_roles_formatter,
    }

    fmt.print_list(plans, fields, formatters, outfile=outfile)


@utils.arg('plan', metavar="<PLAN>",
           help="UUID of the Plan to show.")
def do_plan_show(tuskar, args, outfile=sys.stdout):
    """Show an individual Plan by its UUID."""
    plan = utils.find_resource(tuskar.plans, args.plan)
    print_plan_detail(plan, outfile=outfile)


@utils.arg('plan', metavar="<PLAN>",
           help="UUID of the Plan to show a scale.")
def do_plan_show_scale(tuskar, args, outfile=sys.stdout):
    """Show scale counts of Plan."""
    plan = utils.find_resource(tuskar.plans, args.plan)
    scales = dict()

    for param in plan.parameters:
        if param['name'].endswith('::count'):
            scales[param['name'].replace('::count', '')] = param["value"]

    fmt.print_dict(scales, outfile=outfile)


def print_plan_detail(plan, outfile=sys.stdout):
    """Print detailed Plan information (for plan-show etc.)."""

    formatters = {
        'roles': fmt.parameters_v2_formatter,
        'parameters': fmt.parameters_v2_formatter,
    }
    plan_dict = plan.to_dict()
    fmt.print_dict(plan_dict, formatters, outfile=outfile)


@utils.arg('plan', metavar="<PLAN>",
           help="UUID of the plan to delete.")
def do_plan_delete(tuskar, args, outfile=sys.stdout):
    """Delete an plan by its UUID."""
    plan = utils.find_resource(tuskar.plans, args.plan)
    tuskar.plans.delete(plan.uuid)
    print(u'Deleted Plan "%s".' % plan.name, file=outfile)


@utils.arg('name', help="Name of the Plan to create.")
@utils.arg('-d', '--description', metavar="<DESCRIPTION>",
           help='User-readable text describing the Plan.')
def do_plan_create(tuskar, args, outfile=sys.stdout):
    """Create a new plan."""
    plan = tuskar.plans.create(
        name=vars(args).get('name'),
        description=vars(args).get('description')
    )
    print_plan_detail(plan, outfile=outfile)


@utils.arg('plan_uuid', help="UUID of the Plan to assign role to.")
@utils.arg('-r', '--role-uuid', metavar="<ROLE UUID>",
           required=True, help='UUID of the Role to be assigned.')
def do_plan_add_role(tuskar, args, outfile=sys.stdout):
    """Associate role to a plan."""
    plan = tuskar.plans.add_role(
        vars(args).get('plan_uuid'),
        vars(args).get('role_uuid')
    )
    print_plan_detail(plan, outfile=outfile)


@utils.arg('plan_uuid', help="UUID of the Plan to remove role from.")
@utils.arg('-r', '--role-uuid', metavar="<ROLE UUID>",
           required=True, help='UUID of the Role to be removed.')
def do_plan_remove_role(tuskar, args, outfile=sys.stdout):
    """Remove role from a plan."""
    plan = tuskar.plans.remove_role(
        vars(args).get('plan_uuid'),
        vars(args).get('role_uuid')
    )
    print_plan_detail(plan, outfile=outfile)


@utils.arg('role_name', help="Name of role which you want scale.")
@utils.arg('plan_uuid', help="UUID of the Plan to modify.")
@utils.arg('-C', '--count', metavar='<KEY1=VALUE1>')
def do_plan_scale(tuskar, args, outfile=sys.stdout):
    """Scale plan by changing count of roles."""
    roles = tuskar.roles.list()
    plan = utils.find_resource(tuskar.plans, args.plan_uuid)
    attributes = []

    for role in roles:
        versioned_name = role.name + '-' + str(role.version)
        if versioned_name == args.role_name:
            role_name_key = versioned_name + "::count"
            attributes.append({'name': role_name_key,
                               'value': args.count})
            old_val = [p['value'] for p in plan.parameters
                       if p['name'] == role_name_key][0]

            if old_val != args.count:
                print("Scaling " + args.role_name + " count: " + old_val +
                      " -> " + args.count, file=outfile)
            else:
                print("Keeping scale " + args.role_name + " count: " + old_val,
                      file=outfile)
                return

    if attributes:
        return tuskar.plans.patch(args.plan_uuid, attributes)
    else:
        print("ERROR: no valid plan's roles to scale.", file=sys.stderr)


@utils.arg('plan_uuid', help="UUID of the Plan to modify.")
@utils.arg('-A', '--attribute', dest='attributes', metavar='<KEY1=VALUE1>',
           help='This can be specified multiple times.',
           action='append')
def do_plan_patch(tuskar, args, outfile=sys.stdout):
    attributes = [{'name': pair[0], 'value': pair[1]}
                  for pair
                  in utils.format_attributes(args.attributes).items()]
    return tuskar.plans.patch(args.plan_uuid, attributes)


@utils.arg('plan_uuid',
           help="UUID of the Plan whose Templates will be retrieved.")
@utils.arg('-O', '--output-dir', metavar='<OUTPUT DIR>',
           required=True,
           help='Directory to write template files into. ' +
           'It will be created if it does not exist.')
def do_plan_templates(tuskar, args, outfile=sys.stdout):
    # check that output directory exists and we can write into it
    output_dir = args.output_dir

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # retrieve templates
    templates = tuskar.plans.templates(args.plan_uuid)

    # write file for each key-value in templates
    print("Following templates has been written:")
    for template_name, template_content in templates.items():
        filename = os.path.join(output_dir, template_name)
        with open(filename, 'w+') as template_file:
            template_file.write(template_content)
        print(filename)
