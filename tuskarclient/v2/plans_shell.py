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
@utils.arg('--verbose', default=False, action="store_true",
           help="Display full plan details")
def do_plan_show(tuskar, args, outfile=sys.stdout):
    """Show an individual Plan by its UUID."""
    plan = utils.find_resource(tuskar.plans, args.plan)
    if args.verbose:
        print_plan_detail(plan, outfile=outfile)
    else:
        print_plan_summary(plan, outfile=outfile)


def print_plan_summary(plan, outfile=sys.stdout):
    """Print a summary of Plan information (for plan-show etc.)."""

    formatters = {
        'roles': fmt.parameters_v2_formatter,
        'parameters': fmt.parameters_v2_formatter,
    }
    plan_dict = plan.to_dict()
    plan_dict['parameters'] = [param for param in
                               plan_dict['parameters']
                               if param['name'].endswith('::count')]
    fmt.print_dict(plan_dict, formatters, outfile=outfile)


@utils.arg('plan', metavar="<PLAN>",
           help="UUID of the Plan to show a scale.")
def do_plan_show_scale(tuskar, args, outfile=sys.stdout):
    """Show scale counts of Plan."""
    plan = utils.find_resource(tuskar.plans, args.plan)
    scales = filter_parameters_to_dict(plan.parameters, 'count')
    fmt.print_dict(scales, outfile=outfile)


@utils.arg('plan', metavar="<PLAN>",
           help="UUID of the Plan to show a scale.")
def do_plan_show_flavors(tuskar, args, outfile=sys.stdout):
    """Show flavors assigned to roles of Plan."""
    plan = utils.find_resource(tuskar.plans, args.plan)
    flavors = filter_parameters_to_dict(plan.parameters, 'Flavor')
    fmt.print_dict(flavors, outfile=outfile)


def filter_parameters_to_dict(parameters, param_name):
    """Filters list of parameters for given parameter name suffix."""
    filtered_params = {}
    suffix = '::{0}'.format(param_name)
    for param in parameters:
        if param['name'].endswith(suffix):
            filtered_params[param['name'].replace(suffix, '')] = param["value"]
    return filtered_params


def print_plan_detail(plan, outfile=sys.stdout):
    """Print detailed Plan information (for plan-show --verbose etc.)."""

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
    print_plan_summary(plan, outfile=outfile)


@utils.arg('plan_uuid', help="UUID of the Plan to assign role to.")
@utils.arg('-r', '--role-uuid', metavar="<ROLE UUID>",
           required=True, help='UUID of the Role to be assigned.')
def do_plan_add_role(tuskar, args, outfile=sys.stdout):
    """Associate role to a plan."""
    plan = tuskar.plans.add_role(
        vars(args).get('plan_uuid'),
        vars(args).get('role_uuid')
    )
    print_plan_summary(plan, outfile=outfile)


@utils.arg('plan_uuid', help="UUID of the Plan to remove role from.")
@utils.arg('-r', '--role-uuid', metavar="<ROLE UUID>",
           required=True, help='UUID of the Role to be removed.')
def do_plan_remove_role(tuskar, args, outfile=sys.stdout):
    """Remove role from a plan."""
    plan = tuskar.plans.remove_role(
        vars(args).get('plan_uuid'),
        vars(args).get('role_uuid')
    )
    print_plan_summary(plan, outfile=outfile)


@utils.arg('role_name', help="Name of role which you want scale.")
@utils.arg('plan_uuid', help="UUID of the Plan to modify.")
@utils.arg('-C', '--count', help="Count of nodes to be set.", required=True)
def do_plan_scale(tuskar, args, outfile=sys.stdout):
    """Scale plan by changing count of roles."""
    roles = tuskar.roles.list()
    plan = utils.find_resource(tuskar.plans, args.plan_uuid)
    parameters = []

    for role in roles:
        versioned_name = "{name}-{v}".format(name=role.name, v=role.version)
        if versioned_name == args.role_name:
            role_name_key = versioned_name + "::count"
            parameters.append({'name': role_name_key,
                               'value': args.count})
            old_val = [p['value'] for p in plan.parameters
                       if p['name'] == role_name_key][0]

            if old_val != args.count:
                print("Scaling {role} count: {old_val} -> {new_val}".format(
                      role=args.role_name, old_val=old_val, new_val=args.count
                      ), file=outfile)
            else:
                print("Keeping scale {role} count: {count}".format(
                      role=args.role_name, count=old_val), file=outfile)
                return

    if parameters:
        return tuskar.plans.patch(args.plan_uuid, parameters)
    else:
        print("ERROR: no roles were found in the Plan with the name {0}".
              format(args.role_name), file=sys.stderr)


@utils.arg('role_name', help="Name of role which you want to flavor.")
@utils.arg('plan_uuid', help="UUID of the Plan to modify.")
@utils.arg('-F', '--flavor', help="Flavor which shall be assigned to role.",
           required=True)
def do_plan_flavor(tuskar, args, outfile=sys.stdout):
    """Change flavor of role in the plan."""
    roles = tuskar.roles.list()
    plan = utils.find_resource(tuskar.plans, args.plan_uuid)
    parameters = []

    for role in roles:
        versioned_name = "{name}-{v}".format(name=role.name, v=role.version)
        if versioned_name == args.role_name:
            role_name_key = versioned_name + "::Flavor"
            parameters.append({'name': role_name_key,
                               'value': args.flavor})
            old_val = [p['value'] for p in plan.parameters
                       if p['name'] == role_name_key][0]

            if old_val != args.flavor:
                print("Changing {role} flavor: {old_val} -> {new_val}".format(
                      role=args.role_name, old_val=old_val, new_val=args.flavor
                      ), file=outfile)
            else:
                print("Keeping flavor {role} unchanged: {flavor}".format(
                      role=args.role_name, flavor=old_val), file=outfile)
                return

    if parameters:
        return tuskar.plans.patch(args.plan_uuid, parameters)
    else:
        print("ERROR: no roles were found in the Plan with the name {0}".
              format(args.role_name), file=sys.stderr)


@utils.arg('plan_uuid', help="UUID of the Plan to modify.")
@utils.arg('-A', '--attribute', dest='attributes', metavar='<KEY1=VALUE1>',
           help=('This can be specified multiple times. This argument is '
                 'deprecated, use -P and --parameter instead.'),
           action='append')
@utils.arg('-P', '--parameter', dest='parameters', metavar='<KEY1=VALUE1>',
           help='This can be specified multiple times.',
           action='append')
def do_plan_update(tuskar, args, outfile=sys.stdout):
    """Change an existing plan."""

    parameters = args.parameters

    if args.attributes:
        print("WARNING: The attribute flags -A and --attribute are"
              " deprecated and will be removed in a later release."
              " Use -P and --parameter instead.", file=sys.stderr)
        parameters = args.attributes

    parameters = [{'name': pair[0], 'value': pair[1]}
                  for pair
                  in utils.format_attributes(parameters).items()]
    return tuskar.plans.patch(args.plan_uuid, parameters)


@utils.arg('plan_uuid', help="UUID of the Plan to modify.")
@utils.arg('-A', '--attribute', dest='attributes', metavar='<KEY1=VALUE1>',
           help='This can be specified multiple times.',
           action='append')
def do_plan_patch(*args, **kwargs):
    """Change an existing plan [Deprecated]."""
    print("WARNING: plan-patch method is deprecated"
          " and will be removed in a later release."
          " Use plan-update instead.", file=sys.stderr)
    do_plan_update(*args, **kwargs)


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
    print("The following templates will be written:")
    for template_name, template_content in templates.items():

        # It's possible to organize the role templates and their dependent
        # files into directories, in which case the template_name will carry
        # the directory information. If that's the case, first create the
        # directory structure (if it hasn't already been created by another
        # file in the templates list).
        template_dir = os.path.dirname(template_name)
        output_template_dir = os.path.join(output_dir, template_dir)
        if template_dir and not os.path.exists(output_template_dir):
            os.makedirs(output_template_dir)

        filename = os.path.join(output_dir, template_name)
        with open(filename, 'w+') as template_file:
            template_file.write(template_content)
        print(filename)
