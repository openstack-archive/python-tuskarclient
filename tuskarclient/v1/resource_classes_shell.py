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


def do_resource_class_list(tuskar, args):
    resource_classes = tuskar.resource_classes.list()
    fields = ['id', 'name', 'service_type', 'racks']
    labels = {'racks': '# of racks'}
    formatters = {'racks': len}

    fmt.print_list(resource_classes, fields, formatters, labels)


@utils.arg('id', metavar="<NAME or ID>",
           help="Name or ID of resource class to show.")
def do_resource_class_show(tuskar, args):
    resource_class = fetch_resource_class(tuskar, args.id)
    print_resource_class_detail(resource_class)


@utils.arg('name', help="Name of the resource class to create.")
@utils.arg('--service-type', required=True,
           help="Service type of the resource class to create.")
def do_resource_class_create(tuskar, args):
    resource_class_dict = {
        'name': args.name,
        'service_type': args.service_type,
    }

    resource_class = tuskar.resource_classes.create(**resource_class_dict)
    print_resource_class_detail(resource_class)


@utils.arg('id', metavar="<NAME or ID>",
           help="Name or id of the resource class to update.")
@utils.arg('--service-type',
           help="Service type of the resource class to update.")
@utils.arg('--name',
           help="Name of the resource class to update.")
def do_resource_class_update(tuskar, args):
    resource_class_dict = {
        'name': args.name,
        'service_type': args.service_type,
    }

    fetch_resource_class(tuskar, args.id)

    resource_class = tuskar.resource_classes.update(args.id,
                                                    **resource_class_dict)
    print_resource_class_detail(resource_class)


@utils.arg('id', metavar="<NAME or ID>",
           help="Name or id of the resource class to delete.")
def do_resource_class_delete(tuskar, args):
    resource_class = fetch_resource_class(tuskar, args.id)
    tuskar.resource_classes.delete(args.id)
    print('Deleted resource class "%s".' % resource_class.name)


def print_resource_class_detail(resource_class):
    formatters = {
        'links': fmt.links_formatter,
        'flavors': fmt.resource_links_formatter,
        'racks': fmt.resource_links_formatter,
    }

    resource_class_dict = resource_class.to_dict()

    fmt.print_dict(resource_class_dict, formatters)


def fetch_resource_class(tuskar, resource_class_id):
    try:
        resource_class = utils.find_resource(tuskar.resource_classes,
                                             resource_class_id)
    except exc.HTTPNotFound:
        raise exc.CommandError(
            "Resource Class not found: %s" % resource_class_id)

    return resource_class
