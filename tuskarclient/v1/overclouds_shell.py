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


@utils.arg('overcloud', metavar="<OVERCLOUD>",
           help="ID or name of the Overcloud to show.")
def do_overcloud_show(tuskar, args, outfile=sys.stdout):
    """Show an individual Overcloud by its ID or name."""
    overcloud = utils.find_resource(tuskar.overclouds, args.overcloud)
    print_overcloud_detail(overcloud, outfile=outfile)


def do_overcloud_list(tuskar, args, outfile=sys.stdout):
    """Show a list of the Overclouds."""
    overclouds = tuskar.overclouds.list()
    fields = ['id', 'name', 'description', 'stack_id', 'attributes', 'counts']

    formatters = {
        'attributes': fmt.attributes_formatter,
        'counts': fmt.counts_formatter,
    }

    fmt.print_list(overclouds, fields, formatters, outfile=outfile)


@utils.arg('name', help="Name of the Overcloud to create.")
@utils.arg('-d', '--description', metavar="<DESCRIPTION>",
           help='User-readable text describing the overcloud.')
@utils.arg('-s', '--stack-id', metavar="<STACK ID>",
           help='UID of the stack in Heat.')
@utils.arg('-A', '--attribute', dest='attributes', metavar='<KEY1=VALUE1>',
           help='This can be specified multiple times.',
           action='append')
@utils.arg('-R', '--role-count', dest='roles',
           metavar='<ROLE NAME_OR_ID=COUNT>',
           help='This can be specified multiple times.',
           action='append')
def do_overcloud_create(tuskar, args, outfile=sys.stdout):
    """Create a new Overcloud."""
    overcloud_roles = tuskar.overcloud_roles.list()
    overcloud_dict = create_overcloud_dict(args, overcloud_roles)
    overcloud = tuskar.overclouds.create(**overcloud_dict)
    print_overcloud_detail(overcloud, outfile=outfile)


@utils.arg('overcloud', metavar="<OVERCLOUD>",
           help="ID or name of the Overcloud to update.")
@utils.arg('-n', '--name', metavar="<NAME>",
           help='Name of the Overcloud Role to update.')
@utils.arg('-d', '--description', metavar="<DESCRIPTION>",
           help='User-readable text describing the overcloud.')
@utils.arg('-s', '--stack-id', metavar="<STACK ID>",
           help='UID of the stack in Heat.')
@utils.arg('-A', '--attribute', dest='attributes', metavar='<KEY1=VALUE1>',
           help='This can be specified multiple times.',
           action='append')
@utils.arg('-R', '--role-count', dest='roles',
           metavar='<ROLE NAME_OR_ID=COUNT>',
           help='This can be specified multiple times.',
           action='append')
def do_overcloud_update(tuskar, args, outfile=sys.stdout):
    """Update an existing Overcloud by its ID or name."""
    overcloud = utils.find_resource(tuskar.overclouds, args.overcloud)
    overcloud_roles = tuskar.overcloud_roles.list()
    overcloud_dict = create_overcloud_dict(args, overcloud_roles)
    updated_overcloud = tuskar.overclouds.update(overcloud.id,
                                                 **overcloud_dict)
    print_overcloud_detail(updated_overcloud, outfile=outfile)


@utils.arg('overcloud', metavar="<OVERCLOUD>",
           help="ID or name of the Overcloud to delete.")
def do_overcloud_delete(tuskar, args, outfile=sys.stdout):
    """Delete an Overcloud by its ID or name."""
    overcloud = utils.find_resource(tuskar.overclouds, args.overcloud)
    tuskar.overclouds.delete(overcloud.id)
    print(u'Deleted Overcloud "%s".' % overcloud.name, file=outfile)


def do_overcloud_show_template_parameters(tuskar, args, outfile=sys.stdout):
    """Show the template parameters stored in the Tuskar API."""
    template_parameters = tuskar.overclouds.template_parameters()
    formatters = {
        '*': fmt.attributes_formatter
    }
    template_parameters_dict = template_parameters.to_dict()
    fmt.print_dict(template_parameters_dict, formatters, outfile=outfile)


def create_overcloud_dict(args, roles):
    """Marshal command line arguments to an API request dict.

    :param roles: list of OvercloudRole instances retrieved from the tuskar
                  client
    :type  roles: list of OvercloudRole
    """
    overcloud_dict = {}
    simple_fields = ['name', 'description']
    for field_name in simple_fields:
        field_value = vars(args).get(field_name)
        if field_value is not None:
            overcloud_dict[field_name] = field_value

    overcloud_dict['attributes'] = utils.format_attributes(args.attributes)

    role_name_ids = dict((r.to_dict()['name'], r.to_dict()['id'])
                         for r in roles)
    overcloud_dict['counts'] = utils.format_roles(args.roles, role_name_ids)

    utils.marshal_association(args, overcloud_dict, 'resource_class')
    return overcloud_dict


def print_overcloud_detail(overcloud, outfile=sys.stdout):
    """Print detailed overcloud information (for overcloud-show etc.)."""

    formatters = {
        'attributes': fmt.attributes_formatter,
        'counts': fmt.counts_formatter,
    }
    overcloud_dict = overcloud.to_dict()
    fmt.print_dict(overcloud_dict, formatters, outfile=outfile)
