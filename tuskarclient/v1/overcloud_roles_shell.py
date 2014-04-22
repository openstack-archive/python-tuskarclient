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


@utils.arg('role', metavar="<ROLE>",
           help="ID or name of the Overcloud Role to show.")
def do_overcloud_role_show(tuskar, args, outfile=sys.stdout):
    """Show an individual Overcloud Role by its ID or name."""
    overcloud_role = utils.find_resource(tuskar.overcloud_roles, args.role)
    print_role_detail(overcloud_role, outfile=outfile)


def do_overcloud_role_list(tuskar, args, outfile=sys.stdout):
    """Show a list of the Overcloud Roles."""
    overcloud_roles = tuskar.overcloud_roles.list()
    fields = ['id', 'name', 'image_name', 'flavor_id']
    fmt.print_list(overcloud_roles, fields, outfile=outfile)


@utils.arg('name', help="Name of the Overcloud Role to create.")
@utils.arg('-d', '--description', metavar="<DESCRIPTION>",
           help='User-readable text describing the overcloud.')
@utils.arg('-i', '--image-name', metavar="<IMAGE NAME>",
           help='Name of the image in Glance to be used for this Role.')
@utils.arg('-f', '--flavor-id', metavar="<FLAVOR ID>",
           help='UUID of the flavor of node this role should be deployed on.')
def do_overcloud_role_create(tuskar, args, outfile=sys.stdout):
    """Create a new Overcloud Role."""
    overcloud_role_dict = create_overcloud_role_dict(args)
    overcloud_role = tuskar.overcloud_roles.create(**overcloud_role_dict)
    print_role_detail(overcloud_role, outfile=outfile)


@utils.arg('role', metavar="<ROLE>",
           help="ID or name of the Overcloud Role to update.")
@utils.arg('-n', '--name', metavar="<NAME>",
           help='Name of the Overcloud Role to update.')
@utils.arg('-d', '--description', metavar="<DESCRIPTION>",
           help='User-readable text describing the overcloud.')
@utils.arg('-i', '--image-name', metavar="<IMAGE NAME>",
           help='Name of the image in Glance to be used for this Role.')
@utils.arg('-f', '--flavor-id', metavar="<FLAVOR ID>",
           help='UUID of the flavor of node this role should be deployed on.')
def do_overcloud_role_update(tuskar, args, outfile=sys.stdout):
    """Update an existing Overcloud Role by its ID or name."""
    overcloud_role = utils.find_resource(tuskar.overcloud_roles, args.role)
    overcloud_role_dict = create_overcloud_role_dict(args)
    updated_overcloud_role = tuskar.overcloud_roles.update(
        overcloud_role.id,
        **overcloud_role_dict
    )
    print_role_detail(updated_overcloud_role, outfile=outfile)


@utils.arg('role', metavar="<ROLE>",
           help="ID or name of the Overcloud Role to delete.")
def do_overcloud_role_delete(tuskar, args, outfile=sys.stdout):
    """Delete an Overcloud Role by its ID or name."""
    overcloud_role = utils.find_resource(tuskar.overcloud_roles, args.role)
    tuskar.overcloud_roles.delete(overcloud_role.id)
    print(u'Deleted Overcloud Role "%s".' % overcloud_role.name, file=outfile)


def create_overcloud_role_dict(args):
    """Marshal command line arguments to an API request dict."""
    overcloud_role_dict = {}
    simple_fields = ['name', 'description', 'image_name', 'flavor_id']
    for field_name in simple_fields:
        field_value = vars(args)[field_name]
        if field_value is not None:
            overcloud_role_dict[field_name] = field_value

    utils.marshal_association(args, overcloud_role_dict, 'resource_class')

    return overcloud_role_dict


def print_role_detail(overcloud_role, outfile=sys.stdout):
    """Print detailed Overcloud Role information (overcloud-role-show etc.)."""

    overcloud_role_dict = overcloud_role.to_dict()
    fmt.print_dict(overcloud_role_dict, outfile=outfile)
