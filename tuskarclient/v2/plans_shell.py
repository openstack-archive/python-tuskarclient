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
