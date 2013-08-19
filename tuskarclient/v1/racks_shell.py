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

from tuskarclient import exc
from tuskarclient.common import utils
import tuskarclient.common.formatting as fmt


# TODO(jistr): This is PoC, not final implementation
@utils.arg('id', metavar="<NAME or ID>", help="Name or ID of rack to show.")
def do_rack_show(tuskar, args):
    try:
        rack = utils.find_resource(tuskar.racks, args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError("Rack not found: %s" % args.id)
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


# TODO(jistr): This is PoC, not final implementation
def do_rack_list(tuskar, args):
    racks = tuskar.racks.list()
    fields = ['name', 'subnet', 'state', 'nodes']
    labels = {'nodes': '# of nodes'}
    formatters = {'nodes': fmt.len_formatter}

    fmt.print_list(racks, fields, formatters, labels)
