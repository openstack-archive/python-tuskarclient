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

import os
import sys
import uuid

from tuskarclient import exc
from tuskarclient.openstack.common import importutils


def define_commands_from_module(subparsers, command_module):
    '''Find all methods beginning with 'do_' in a module, and add them
    as commands into a subparsers collection.
    '''
    for method_name in (a for a in dir(command_module) if a.startswith('do_')):
        # Commands should be hypen-separated instead of underscores.
        command = method_name[3:].replace('_', '-')
        callback = getattr(command_module, method_name)
        define_command(subparsers, command, callback)


def define_command(subparsers, command, callback):
    '''Define a command in the subparsers collection.

    :param subparsers: subparsers collection where the command will go
    :param command: command name
    :param callback: function that will be used to process the command
    '''
    desc = callback.__doc__ or ''
    help = desc.strip().split('\n')[0]
    arguments = getattr(callback, 'arguments', [])

    subparser = subparsers.add_parser(command, help=help, description=desc)
    for (args, kwargs) in arguments:
        subparser.add_argument(*args, **kwargs)
    subparser.set_defaults(func=callback)


# Decorator for cli-args
def arg(*args, **kwargs):
    def _decorator(func):
        # Because of the sematics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        func.__dict__.setdefault('arguments', []).insert(0, (args, kwargs))
        return func
    return _decorator


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
        # This is temporary measure to prevent ugly errors on CLI.
        # Make this just 'pass' after we implement finding by name.
        msg = "No %s with ID of '%s' exists." % \
              (manager.resource_class.__name__.lower(), name_or_id)
        raise exc.CommandError(msg)

    # finally try to find entity by name
    try:
        return manager.find(name=name_or_id)
    except exc.NotFound:
        msg = "No %s with a name or ID of '%s' exists." % \
              (manager.resource_class.__name__.lower(), name_or_id)
        raise exc.CommandError(msg)


def marshal_association(args, resource_dict, assoc_name):
    """Marshal resource association into an API request dict.

    Distinguish between 3 cases:

    - when the value in args is present, set the value in dict too,
    - when the value in args is an empty string, set the value in dict
      to none,
    - when the value in args is None, it means the user did not specify
      it on the command line and it should not be present in the dict
      (important for update).
    """
    assoc_value = getattr(args, assoc_name, None)
    if assoc_value == '':
        resource_dict[assoc_name] = None
    elif assoc_value:
        # TODO(jistr): support for selecting resources by name
        resource_dict[assoc_name] = {'id': assoc_value}


def string_to_bool(arg):
    return arg.strip().lower() in ('t', 'true', 'yes', '1')


def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars

    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.
    """
    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
    return kwargs.get('default', '')


def import_versioned_module(version, submodule=None):
    module = 'tuskarclient.v%s' % version
    if submodule:
        module = '.'.join((module, submodule))
    return importutils.import_module(module)


def exit(msg=''):
    if msg:
        print >> sys.stderr, msg
    sys.exit(1)
