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


def attributes_formatter(attributes):
    """Given a simple dict format the keyvalue pairs with one on each line.
    """
    return u"".join(u"{0}={1}\n".format(k, v) for k, v in
                    sorted(attributes.items()))


def parameters_v2_formatter(parameters):
    """Given a list of dicts format parameters output."""
    return u"\n".join(attributes_formatter(parameter)
                      for parameter in parameters)


def list_plan_roles_formatter(roles):
    """Given a list of Roles format roles' names into row."""
    return u", ".join(role.name for role in roles)
