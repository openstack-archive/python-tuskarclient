# Copyright 2012 OpenStack LLC.
# All Rights Reserved.
#
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

import sys
import uuid

from oslo_utils import importutils

from tuskarclient.openstack.common.apiclient import exceptions as exc
from tuskarclient.openstack.common import cliutils
from tuskarclient.openstack.common.gettextutils import _

# Using common methods from oslo cliutils
arg = cliutils.arg
env = cliutils.env


def define_commands_from_module(subparsers, command_module):
    """Find all methods beginning with 'do_' in a module, and add them
    as commands into a subparsers collection.
    """
    for method_name in (a for a in dir(command_module) if a.startswith('do_')):
        # Commands should be hypen-separated instead of underscores.
        command = method_name[3:].replace('_', '-')
        callback = getattr(command_module, method_name)
        define_command(subparsers, command, callback)


def define_command(subparsers, command, callback):
    """Define a command in the subparsers collection.

    :param subparsers: subparsers collection where the command will go
    :param command: command name
    :param callback: function that will be used to process the command
    """
    desc = callback.__doc__ or ''
    help = desc.strip().split('\n')[0]
    arguments = getattr(callback, 'arguments', [])

    subparser = subparsers.add_parser(command, help=help, description=desc)
    for (args, kwargs) in arguments:
        subparser.add_argument(*args, **kwargs)
    subparser.set_defaults(func=callback)


def find_resource(manager, name_or_id):
    """Helper for the _find_* methods."""
    # first try to get entity as integer id
    try:
        if isinstance(name_or_id, int) or name_or_id.isdigit():
            return manager.get(int(name_or_id))
    except exc.NotFound:
        pass

    # now try to get entity as uuid
    try:
        uuid.UUID(str(name_or_id))
        return manager.get(name_or_id)
    except (ValueError, exc.NotFound):
        pass

    # finally try to find the entity by name
    resource = getattr(manager, 'resource_class', None)
    attr = resource.NAME_ATTR if resource else 'name'

    listing = manager.list()
    matches = [obj for obj in listing if getattr(obj, attr) == name_or_id]

    num_matches = len(matches)
    if num_matches == 0:
        msg = "No %s with name '%s' exists." % (
              manager.resource_class.__name__.lower(), name_or_id)
        raise exc.CommandError(msg)
    elif num_matches > 1:
        msg = "Multiple instances of %s with name '%s' exist." % (
              manager.resource_class.__name__.lower(), name_or_id)
        raise exc.CommandError(msg)

    return matches[0]


def import_versioned_module(version, submodule=None):
    module = 'tuskarclient.v%s' % version
    if submodule:
        module = '.'.join((module, submodule))
    return importutils.import_module(module)


def format_key_value(params):
    """Parse a list of k=v strings into an iterator of (k,v).

    :raises: CommandError
    """
    if not params:
        raise StopIteration

    for param in params:
        try:
            (name, value) = param.split(('='), 1)
        except ValueError:
            msg = _('Malformed parameter({0}). Use the key=value format.')
            raise exc.CommandError(msg.format(param))
        yield name, value


def format_key_value_args(params):
    """Reformat CLI attributes into the structure expected by the API.

    The format expected by the API for attributes is a dictionary consisting
    of only string keys and values.

    :raises: ValidationError
    """
    attributes = {}

    for key, value in format_key_value(params):

        if key in attributes:
            raise exc.ValidationError(
                _("The attribute name {0} can't be given twice.").format(key))

        attributes[key] = value

    return attributes


def parameters_args_to_patch(parameters):
    """Create a list of patch dicts to update the parameters in the API."""

    return [{'name': pair[0], 'value': pair[1]}
            for pair in sorted(format_key_value_args(parameters).items())]


def args_to_patch(flavors, roles, parameter):
    """Create a list of dicts to update the given parameter in the API."""

    role_flavors_dict = format_key_value_args(flavors)

    roles = dict(("{0}-{1}".format(r.name, r.version), r) for r in roles)
    patch = []

    for role_name, flavor in sorted(role_flavors_dict.items()):

        if role_name in roles:
            patch.append({
                'name': "{0}::{1}".format(role_name, parameter),
                'value': flavor
            })
        else:
            print("ERROR: no roles were found in the Plan with the name {0}".
                  format(role_name), file=sys.stderr)
            continue

    return patch
