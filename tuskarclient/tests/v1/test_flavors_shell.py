# Copyright (c) 2013 Red Hat, Inc.
# All Rights Reserved.

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

import mock

import tuskarclient.tests.utils as tutils
from tuskarclient.v1 import flavors_shell


class FlavorsShellListTest(tutils.TestCase):

    def empty_args(self):
        args = mock.Mock(spec=[])
        for attr in ['id', 'resource_class_id', 'capacities', 'max_vms']:
            setattr(args, attr, None)
        return args

    @mock.patch.object(flavors_shell, 'fetch_resource_class')
    @mock.patch.object(flavors_shell, 'fmt')
    def test_list_works_if_resource_class_exists(
            self, mocked_fmt, mocked_fetch_resource_class):
        tuskar = mock.MagicMock()
        args = self.empty_args()
        args.resource_class_id = 1

        flavors_shell.do_flavor_list(tuskar, args)
        tuskar.flavors.list.assert_called_with(
            mocked_fetch_resource_class.return_value.id)
        mocked_fmt.print_list.assert_called_with(
            tuskar.flavors.list.return_value,
            mock.ANY, mock.ANY, mock.ANY
        )

    def test_show_works_with_integer_id(self):
        self.show_works_with_id({'resource_class_id': 1,
                                 'flavor_id': 1})

    def test_show_works_with_char_id(self):
        self.show_works_with_id({'resource_class_id': 1,
                                 'flavor_id': '1'})

    def test_show_works_with_string_id(self):
        self.show_works_with_id({'resource_class_id': 1,
                                 'flavor_id': 'string'})

    @mock.patch.object(flavors_shell, 'fetch_flavor')
    @mock.patch.object(flavors_shell, 'print_flavor_detail')
    def show_works_with_id(self,
                           parameters,
                           mocked_print_flavor_detail,
                           mocked_fetch_flavor):
        flavor_id = parameters.get('flavor_id')
        resource_class_id = parameters.get('resource_class_id')
        tuskar = mock.MagicMock()
        args = self.empty_args()
        args.id = flavor_id
        args.resource_class_id = resource_class_id

        flavors_shell.do_flavor_show(tuskar, args)
        mocked_fetch_flavor.assert_called_with(tuskar,
                                               resource_class_id,
                                               args.id)
        mocked_print_flavor_detail.assert_called_with(
            mocked_fetch_flavor.return_value,
        )

    def test_delete_works_with_integer_id(self):
        self.delete_works_with_id({'resource_class_id': 1,
                                   'flavor_id': 1})

    def test_delete_works_with_char_id(self):
        self.delete_works_with_id({'resource_class_id': 1,
                                   'flavor_id': '1'})

    def test_delete_works_with_string_id(self):
        self.delete_works_with_id({'resource_class_id': 1,
                                   'flavor_id': 'string'})

    @mock.patch.object(flavors_shell, 'fetch_flavor')
    def delete_works_with_id(self, parameters, mocked_fetch_flavor):
        flavor_id = parameters.get('flavor_id')
        tuskar = mock.MagicMock()
        args = self.empty_args()
        args.id = flavor_id

        flavors_shell.do_flavor_delete(tuskar, args)
        mocked_fetch_flavor.assert_called_with(tuskar, args.id)
        tuskar.flavors.delete.assert_called_with(args.id)

    def test_create_works_with_name(self):
        self.create_works_with({'resource_class_id': 1,
                                'name': 'name',
                                'capacities': None,
                                'max_vms': None})

    def test_create_works_with_name_and_capacities(self):
        self.create_works_with({'resource_class_id': 1,
                                'name': 'name',
                                'capacities':
                                'total_memory:2048:MB,total_cpu:3:CPU',
                                'max_vms': None})

    @mock.patch.object(flavors_shell, 'fetch_resource_class')
    @mock.patch.object(flavors_shell, 'print_flavor_detail')
    def create_works_with(
            self, parameters, mocked_print_flavor_detail,
            mocked_fetch_resource_class):
        name = parameters.get('name')
        resource_class_id = parameters.get('resource_class_id')
        capacities = parameters.get('capacities')
        max_vms = parameters.get('max_vms')
        tuskar = mock.MagicMock()
        args = self.empty_args()
        args.name = name
        args.resource_class_id = resource_class_id
        args.capacities = capacities
        args.max_vms = max_vms

        expected_params = {
            'name': name,
            'max_vms': max_vms,
        }

        if capacities is not None:
            expected_params['capacities'] = \
                flavors_shell.parse_capacities(capacities)

        mocked_fetch_resource_class.return_value.id = resource_class_id

        flavors_shell.do_flavor_create(tuskar,
                                       args)
        tuskar.flavors.create.assert_called_with(
            resource_class_id,
            **expected_params
        )
        mocked_print_flavor_detail.assert_called_with(
            tuskar.flavors.create.return_value
        )

    def test_update_works_with_integer_id(self):
        self.update_works({'flavor_id': 1,
                           'resource_class_id': 1,
                           'name': None,
                           'capacities': None,
                           'max_vms': None},
                          {})

    def test_update_works_with_char_id(self):
        self.update_works({'flavor_id': '1',
                           'resource_class_id': 1,
                           'name': None,
                           'capacities': None,
                           'max_vms': None},
                          {})

    def test_update_works_with_string_id(self):
        self.update_works({'flavor_id': 'string',
                           'resource_class_id': 1,
                           'name': None,
                           'capacities': None,
                           'max_vms': None},
                          {})

    def test_update_works_with_id_and_name(self):
        self.update_works({'flavor_id': 1,
                           'resource_class_id': 1,
                           'name': 'name',
                           'capacities': None,
                           'max_vms': None},
                          {'name': 'name'})

    def test_update_works_with_id_and_empty_capacities(self):
        self.update_works({'flavor_id': 1,
                           'resource_class_id': 1,
                           'name': None,
                           'capacities': '',
                           'max_vms': None},
                          {'capacities': []})

    def test_update_works_with_id_and_capacities(self):
        self.update_works({'flavor_id': 1,
                           'resource_class_id': 1,
                           'name': None,
                           'capacities':
                           'total_memory:2048:MB,total_cpu:3:CPU',
                           'max_vms': None},
                          {'capacities': [
                              {'unit': 'MB',
                               'name': 'total_memory',
                               'value': '2048'},
                              {'unit': 'CPU',
                               'name': 'total_cpu',
                               'value': '3'}]})

    def test_update_works_with_id_name_and_capacities(self):
        self.update_works({'flavor_id': 1,
                           'resource_class_id': 1,
                           'name': 'name',
                           'capacities':
                           'total_memory:2048:MB,total_cpu:3:CPU',
                           'max_vms': None},
                          {'name': 'name',
                           'capacities': [
                               {'unit': 'MB',
                                'name': 'total_memory',
                                'value': '2048'},
                               {'unit': 'CPU',
                                'name': 'total_cpu',
                                'value': '3'}]})

    @mock.patch.object(flavors_shell, 'fetch_flavor')
    @mock.patch.object(flavors_shell, 'print_flavor_detail')
    def update_works(self,
                     parameters,
                     expected_parameters,
                     mocked_print_flavor_detail,
                     mocked_fetch_flavor):
        flavor_id = parameters.get('flavor_id')
        resource_class_id = parameters.get('resource_class_id')
        name = parameters.get('name')
        capacities = parameters.get('capacities')
        max_vms = parameters.get('max_vms')
        tuskar = mock.MagicMock()
        args = self.empty_args()
        args.id = flavor_id
        args.resource_class_id = resource_class_id
        args.name = name
        args.max_vms = max_vms
        args.capacities = capacities

        flavors_shell.do_flavor_update(tuskar, args)
        mocked_fetch_flavor.assert_called_with(tuskar,
                                               resource_class_id,
                                               args.id)
        tuskar.flavors.update.assert_called_with(
            resource_class_id,
            flavor_id,
            **expected_parameters
        )
        mocked_print_flavor_detail.assert_called_with(
            tuskar.flavors.update.return_value
        )

    @mock.patch.object(flavors_shell.utils, 'find_resource')
    def test_fetch_flavor_works(self,
                                mocked_find_resource):
        tuskar = mock.MagicMock()
        flavor_id = 1
        resource_class_id = 1

        return_value = flavors_shell.fetch_flavor(
            tuskar, resource_class_id, flavor_id)
        tuskar.flavors.get.assert_called_with(resource_class_id,
                                              flavor_id)
        self.assertEqual(return_value, tuskar.flavors.get.return_value)

    @mock.patch.object(flavors_shell.utils, 'find_resource')
    def test_fetch_flavor_blows(self,
                                mocked_find_resource):
        tuskar = mock.MagicMock()
        flavor_id = 1
        resource_class_id = 1
        e = flavors_shell.exc.HTTPNotFound(
            "Flavor not found: 1")

        mocked_find_resource.side_effect = e
        tuskar.flavors.get.side_effect = e
        self.assertRaises(flavors_shell.exc.CommandError,
                          flavors_shell.fetch_flavor,
                          tuskar, resource_class_id, flavor_id)
        tuskar.flavors.get.assert_called_with(resource_class_id,
                                              flavor_id)

    @mock.patch.object(flavors_shell, 'fmt')
    def test_print_flavor_detail_works(self,
                                       mocked_fmt):
        flavor = mock.MagicMock()

        flavors_shell.print_flavor_detail(flavor)
        mocked_fmt.print_dict.assert_called_with(
            flavor.to_dict.return_value,
            mock.ANY)

    def test_create_flavor_dict_works(self):
        args = self.empty_args()
        args.name = 'name-value'
        args.capacities = 'total_memory:2048:MB,total_cpu:3:CPU'
        args.other = 'other-value'

        expected_flavor_dict = {'name': 'name-value',
                                'capacities': [{'name': 'total_memory',
                                                'value': '2048',
                                                'unit': 'MB'},
                                               {'name': 'total_cpu',
                                                'value': '3',
                                                'unit': 'CPU'}]
                                }
        flavor_dict = flavors_shell.create_flavor_dict(args)
        self.assertEqual(flavor_dict, expected_flavor_dict)
