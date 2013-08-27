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

import mock

import tuskarclient.tests.utils as tutils
from tuskarclient.v1 import resource_classes_shell


class ResourceClassesShellListTest(tutils.TestCase):
    def empty_args(self):
        args = mock.Mock(spec=[])
        for attr in ['id', 'service_type']:
            setattr(args, attr, None)

        return args

    @mock.patch.object(resource_classes_shell, 'fmt')
    def test_list_works(self, mocked_fmt):
        tuskar = mock.MagicMock()
        args = self.empty_args()

        resource_classes_shell.do_resource_class_list(tuskar, args)
        tuskar.resource_classes.list.assert_called_with()
        mocked_fmt.print_list.assert_called_with(
            tuskar.resource_classes.list.return_value,
            mock.ANY, mock.ANY, mock.ANY
        )

    def test_show_works_with_integer_id(self):
        self.show_works_with_id(1)

    def test_show_works_with_char_id(self):
        self.show_works_with_id('1')

    def test_show_works_with_string_id(self):
        self.show_works_with_id('string')

    @mock.patch.object(resource_classes_shell, 'fetch_resource_class')
    @mock.patch.object(resource_classes_shell, 'print_resource_class_detail')
    def show_works_with_id(self, resource_class_id,
                           mocked_print_resource_class_detail,
                           mocked_fetch_resource_class):
        tuskar = mock.MagicMock()
        args = self.empty_args()
        args.id = resource_class_id

        resource_classes_shell.do_resource_class_show(tuskar, args)
        mocked_fetch_resource_class.assert_called_with(tuskar, args.id)
        mocked_print_resource_class_detail.assert_called_with(
            mocked_fetch_resource_class.return_value,
        )

    def test_delete_works_with_integer_id(self):
        self.delete_works_with_id(1)

    def test_delete_works_with_char_id(self):
        self.delete_works_with_id('1')

    def test_delete_works_with_string_id(self):
        self.delete_works_with_id('string')

    @mock.patch.object(resource_classes_shell, 'fetch_resource_class')
    def delete_works_with_id(self, resource_class_id,
                             mocked_fetch_resource_class):
        tuskar = mock.MagicMock()
        args = self.empty_args()
        args.id = resource_class_id

        resource_classes_shell.do_resource_class_delete(tuskar, args)
        mocked_fetch_resource_class.assert_called_with(tuskar, args.id)
        tuskar.resource_classes.delete.assert_called_with(args.id)

    def test_create_works_with_name(self):
        self.create_works_with('name', None)

    def test_create_works_with_name_and_service_type(self):
        self.create_works_with('name', 'service_type')

    @mock.patch.object(resource_classes_shell, 'print_resource_class_detail')
    def create_works_with(self,
                          name, service_type,
                          mocked_print_resource_class_detail):
        tuskar = mock.MagicMock()
        args = self.empty_args()
        args.name = name
        args.service_type = service_type

        resource_classes_shell.do_resource_class_create(tuskar, args)
        tuskar.resource_classes.create.assert_called_with(
            name=name,
            service_type=service_type,
        )
        mocked_print_resource_class_detail.assert_called_with(
            tuskar.resource_classes.create.return_value
        )

    def test_update_works_with_integer_id(self):
        self.update_works(1, None, None)

    def test_update_works_with_char_id(self):
        self.update_works('1', None, None)

    def test_update_works_with_string_id(self):
        self.update_works('string', None, None)

    def test_update_works_with_id_and_name(self):
        self.update_works(1, 'name', None)

    def test_update_works_with_id_and_service_type(self):
        self.update_works(1, None, 'service_type')

    def test_update_works_with_id_name_and_service_type(self):
        self.update_works(1, 'name', 'service_type')

    @mock.patch.object(resource_classes_shell, 'fetch_resource_class')
    @mock.patch.object(resource_classes_shell, 'print_resource_class_detail')
    def update_works(self,
                     resource_class_id, name, service_type,
                     mocked_print_resource_class_detail,
                     mocked_fetch_resource_class):
        tuskar = mock.MagicMock()
        args = self.empty_args()
        args.id = resource_class_id
        args.name = name
        args.service_type = service_type

        resource_classes_shell.do_resource_class_update(tuskar, args)

        mocked_fetch_resource_class.assert_called_with(tuskar, args.id)
        tuskar.resource_classes.update.assert_called_with(
            resource_class_id,
            name=name,
            service_type=service_type,
        )
        mocked_print_resource_class_detail.assert_called_with(
            tuskar.resource_classes.update.return_value
        )

    @mock.patch.object(resource_classes_shell.utils, 'find_resource')
    def test_fetch_resource_class_works(self,
                                        mocked_find_resource):
        tuskar = mock.MagicMock()
        resource_class_id = 1

        return_value = resource_classes_shell.fetch_resource_class(
            tuskar, resource_class_id)
        mocked_find_resource.assert_called_with(tuskar.resource_classes,
                                                resource_class_id)
        self.assertEqual(return_value, mocked_find_resource.return_value)

    @mock.patch.object(resource_classes_shell.utils, 'find_resource')
    def test_fetch_resource_class_blows(self,
                                        mocked_find_resource):
        tuskar = mock.MagicMock()
        resource_class_id = 1
        e = resource_classes_shell.exc.HTTPNotFound(
            "Resource Class not found: 1")

        mocked_find_resource.side_effect = e
        self.assertRaises(resource_classes_shell.exc.CommandError,
                          resource_classes_shell.fetch_resource_class,
                          tuskar, resource_class_id)
        mocked_find_resource.assert_called_with(tuskar.resource_classes,
                                                resource_class_id)

    @mock.patch.object(resource_classes_shell, 'fmt')
    def test_print_resource_class_detail_works(self,
                                               mocked_fmt):
        resource_class = mock.MagicMock()

        resource_classes_shell.print_resource_class_detail(resource_class)
        mocked_fmt.print_dict.assert_called_with(
            resource_class.to_dict.return_value,
            mock.ANY)
