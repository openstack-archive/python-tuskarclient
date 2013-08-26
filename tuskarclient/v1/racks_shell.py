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

from __future__ import print_function

import tuskarclient.common.formatting as fmt
from tuskarclient.common import utils
from tuskarclient import exc


@utils.arg('id', metavar="<NAME or ID>", help="Name or ID of rack to show.")
def do_rack_show(tuskar, args):
    rack = utils.find_resource(tuskar.racks, args.id)
    print_rack_detail(rack)


def do_rack_list(tuskar, args):
    racks = tuskar.racks.list()
    fields = ['id', 'name', 'subnet', 'state', 'nodes']
    labels = {'nodes': '# of nodes'}
    formatters = {'nodes': len}
    fmt.print_list(racks, fields, formatters, labels)


@utils.arg('name', help="Name of the rack to create.")
@utils.arg('--subnet', required=True,
           help="Rack's network in IP/CIDR notation.")
@utils.arg('--slots', required=True, help="Number of slots in the rack.")
@utils.arg('--capacities', help="Total capacities of the rack.")
@utils.arg('--resource-class', help="Resource class to assign the rack to.")
def do_rack_create(tuskar, args):
    rack_dict = create_rack_dict(args)
    rack = tuskar.racks.create(**rack_dict)
    print_rack_detail(rack)


@utils.arg('id', metavar="<NAME or ID>", help="Name or ID of rack to show.")
@utils.arg('--name', help="Rack's updated name.")
@utils.arg('--subnet', help="Rack's network in IP/CIDR notation.")
@utils.arg('--capacities', help="Total capacities of the rack.")
@utils.arg('--slots', help="Number of slots in the rack.")
@utils.arg('--resource-class', help="Resource class to assign the rack to.")
def do_rack_update(tuskar, args):
    rack = utils.find_resource(tuskar.racks, args.id)
    rack_dict = create_rack_dict(args)
    updated_rack = tuskar.racks.update(rack.id, **rack_dict)
    print_rack_detail(updated_rack)


@utils.arg('id', metavar="<NAME or ID>", help="Name or ID of rack to show.")
def do_rack_delete(tuskar, args):
    rack = utils.find_resource(tuskar.racks, args.id)
    tuskar.racks.delete(args.id)
    print('Deleted rack "%s".' % rack.name)


def create_rack_dict(args):
    '''Create a rack dict for use with API requests from supplied command
    line args.
    '''
    rack_dict = {}
    simple_fields = ['name', 'subnet', 'slots']
    for field_name in simple_fields:
        field_value = vars(args)[field_name]
        if field_value is not None:
            rack_dict[field_name] = field_value

    if args.resource_class == '':
        rack_dict['resource_class'] = None
    elif args.resource_class:
        # TODO(jistr): support for selecting resource class by name
        rack_dict['resource_class'] = {'id': args.resource_class}

    if args.capacities is not None:
        rack_dict['capacities'] = parse_capacities(args.capacities)

    return rack_dict


def print_rack_detail(rack):
    '''Print detailed rack information (for rack-show etc.).'''
    formatters = {
        'capacities': fmt.capacities_formatter,
        'chassis': fmt.resource_link_formatter,
        'links': fmt.links_formatter,
        'nodes': fmt.resource_links_formatter,
        'resource_class': fmt.resource_link_formatter,
    }

    rack_dict = rack.to_dict()
    # Workaround for API inconsistency, where empty chassis link
    # prints out as '{}'.
    if 'chassis' in rack_dict and not rack_dict['chassis']:
        del rack_dict['chassis']

    fmt.print_dict(rack_dict, formatters)


def parse_capacities(capacities_str):
    '''Take capacities from CLI and parse them into format for API.

    :param capacities_string: string of capacities like
        'total_cpu:64:CPU,total_memory:1024:MB'
    :return: array of capacities dicts usable for requests to API
    '''
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
