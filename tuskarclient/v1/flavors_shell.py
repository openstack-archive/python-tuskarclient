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

import tuskarclient.common.formatting as fmt
from tuskarclient.common import utils
from tuskarclient import exc


@utils.arg('resource_class_id', metavar="<RESOURCE CLASS NAME or ID>",
           help="Name or ID of resource class which flavors to show.")
def do_flavor_list(tuskar, args):
    # TODO(pblaho):
    # temp. fetch resource_class - API do return 200 OK
    # when getting list of flavors for non-existing resource class
    resource_class = fetch_resource_class(tuskar, args.resource_class_id)
    flavors = tuskar.flavors.list(resource_class.id)
    fields = ['id', 'name', 'capacities', 'max_vms']
    labels = {'racks': '# of racks'}
    formatters = {'racks': len, 'capacities': fmt.capacities_formatter}

    fmt.print_list(flavors, fields, formatters, labels)


@utils.arg('resource_class_id', metavar="<RESOURCE CLASS NAME or ID>",
           help="Name or ID of resource class associated to.")
@utils.arg('id', metavar="<FLAVOR NAME or ID>",
           help="Name or ID of the flavor to update.")
def do_flavor_show(tuskar, args):
    fetch_resource_class(tuskar, args.resource_class_id)
    flavor = fetch_flavor(tuskar, args.resource_class_id, args.id)
    print_flavor_detail(flavor)


@utils.arg('resource_class_id', metavar="<RESOURCE CLASS NAME or ID>",
           help="Name or ID of resource class associated to.")
@utils.arg('name',
           help="Name of the flavor to create.")
@utils.arg('--capacities',
           help="Capacities of the flavor to create.")
@utils.arg('--max-vms',
           help="Maximum # of VMs of the flavor to create.")
def do_flavor_create(tuskar, args):
    resource_class = fetch_resource_class(tuskar, args.resource_class_id)
    flavor_dict = {
        'name': args.name,
        'max_vms': args.max_vms,
    }

    if args.capacities is not None:
        flavor_dict['capacities'] = parse_capacities(args.capacities)

    flavor = tuskar.flavors.create(resource_class.id, **flavor_dict)
    print_flavor_detail(flavor)


@utils.arg('resource_class_id', metavar="<RESOURCE CLASS NAME or ID>",
           help="Name or ID of resource class associated to.")
@utils.arg('id', metavar="<FLAVOR NAME or ID>",
           help="Name or ID of the flavor to update.")
@utils.arg('--name',
           help="New name of the flavor to update.")
@utils.arg('--capacities',
           help="Capacities of the flavor to update.")
@utils.arg('--max-vms',
           help="Maximum # of VMs of the flavor to update.")
def do_flavor_update(tuskar, args):
    flavor_dict = create_flavor_dict(args)
    fetch_resource_class(tuskar, args.resource_class_id)
    fetch_flavor(tuskar, args.resource_class_id, args.id)

    flavor = tuskar.flavors.update(args.resource_class_id,
                                   args.id,
                                   **flavor_dict)
    print_flavor_detail(flavor)


def do_flavor_delete(tuskar, args):
    fetch_flavor(tuskar, args.id)

    tuskar.flavors.delete(args.id)


def print_flavor_detail(flavor):
    flavor_dict = flavor.to_dict()
    formatters = {'links': fmt.links_formatter,
                  'capacities': fmt.capacities_formatter,
                  }
    fmt.print_dict(flavor_dict, formatters)


def fetch_flavor(tuskar, resource_class_id, flavor_id):
    try:
        flavor = tuskar.flavors.get(resource_class_id, flavor_id)
    except exc.HTTPNotFound:
        raise exc.CommandError(
            "Flavor not found: %s" % flavor_id)

    return flavor


# TODO(pblaho):
# temp. fetch resource_class - API do return 200 OK
# when getting list of flavors for non-existing resource class
def fetch_resource_class(tuskar, resource_class_id):
    try:
        resource_class = utils.find_resource(tuskar.resource_classes,
                                             resource_class_id)
    except exc.HTTPNotFound:
        raise exc.CommandError(
            "Resource Class not found: %s" % resource_class_id)

    return resource_class


# TODO(pblaho): duplicate now
# refactor after merged both this and https://review.openstack.org/#/c/44281
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


def create_flavor_dict(args):
    flavor_dict = {}

    simple_fields = ['name', 'max_vms']
    for field_name in simple_fields:
        field_value = vars(args)[field_name]
        if field_value is not None:
            flavor_dict[field_name] = field_value

    if args.capacities is not None:
        flavor_dict['capacities'] = parse_capacities(args.capacities)

    return flavor_dict
