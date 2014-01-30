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
from tuskarclient.openstack.common.apiclient import exceptions as exc


@utils.arg('id', metavar="<ID>", help="ID of overcloud to show.")
def do_overcloud_show(tuskar, args, outfile=sys.stdout):
    """ Given a Tuskar client instance and the command line arguments display
    the detail to the user.
    """
    overcloud = utils.find_resource(tuskar.overclouds, args.id)
    print_overcloud_detail(overcloud, outfile=outfile)


def do_overcloud_list(tuskar, args, outfile=sys.stdout):
    overclouds = tuskar.overclouds.list()
    fields = ['id', 'name']
    fmt.print_list(overclouds, fields, outfile=outfile)


@utils.arg('name', help="Name of the overcloud to create.")
def do_overcloud_create(tuskar, args, outfile=sys.stdout):
    overcloud_dict = create_overcloud_dict(args)
    overcloud = tuskar.overclouds.create(**overcloud_dict)
    print_overcloud_detail(overcloud, outfile=outfile)


@utils.arg('id', metavar="<ID>", help="ID of overcloud to show.")
@utils.arg('--name', help="Rack's updated name.")
def do_overcloud_update(tuskar, args, outfile=sys.stdout):
    overcloud = utils.find_resource(tuskar.overclouds, args.id)
    overcloud_dict = create_overcloud_dict(args)
    updated_overcloud = tuskar.overclouds.update(overcloud.id,
                                                 **overcloud_dict)
    print_overcloud_detail(updated_overcloud, outfile=outfile)


@utils.arg('id', metavar="<ID>", help="ID of overcloud to show.")
def do_overcloud_delete(tuskar, args, outfile=sys.stdout):
    overcloud = utils.find_resource(tuskar.overclouds, args.id)
    tuskar.overclouds.delete(args.id)
    print(u'Deleted overcloud "%s".' % overcloud.name, file=outfile)


def create_overcloud_dict(args):
    """Marshal command line arguments to an API request dict."""
    overcloud_dict = {}
    simple_fields = ['id', 'name', ]
    for field_name in simple_fields:
        field_value = vars(args)[field_name]
        if field_value is not None:
            overcloud_dict[field_name] = field_value

    utils.marshal_association(args, overcloud_dict, 'resource_class')

    return overcloud_dict


def print_overcloud_detail(overcloud, outfile=sys.stdout):
    """Print detailed overcloud information (for overcloud-show etc.)."""

    overcloud_dict = overcloud.to_dict()
    fmt.print_dict(overcloud_dict, outfile=outfile)


def parse_capacities(capacities_str):
    """Take capacities from CLI and parse them into format for API.

    :param capacities_string: string of capacities like
        'total_cpu:64:CPU,total_memory:1024:MB'
    :return: array of capacities dicts usable for requests to API
    """
    if capacities_str == '':
        return []

    capacities = []
    for capacity_str in capacities_str.split(','):
        fields = capacity_str.split(':')
        if len(fields) != 3:
            raise exc.CommandError(
                'Capacity info "{0}" should be 3 fields separated by colons. '
                '(Use commas to separate multiple capacities.)'
                .format(capacity_str))
        capacities.append(
            {'name': fields[0], 'value': fields[1], 'unit': fields[2]})

    return capacities
