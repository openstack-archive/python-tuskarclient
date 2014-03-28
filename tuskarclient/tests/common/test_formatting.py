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
import six

import tuskarclient.common.formatting as fmt
import tuskarclient.tests.utils as tutils


class PrintTest(tutils.TestCase):

    def setUp(self):
        super(PrintTest, self).setUp()
        self.outfile = six.StringIO()

    def test_print_dict(self):
        dict_ = {'k': 'v', 'key': 'value'}
        formatters = {'key': lambda v: 'custom ' + v}
        custom_labels = {'k': 'custom_key'}

        fmt.print_dict(dict_, formatters, custom_labels,
                       outfile=self.outfile)
        self.assertEqual(
            ('+------------+--------------+\n'
             '| Property   | Value        |\n'
             '+------------+--------------+\n'
             '| custom_key | v            |\n'
             '| key        | custom value |\n'
             '+------------+--------------+\n'),
            self.outfile.getvalue()
        )

    def test_print_list(self):
        fields = ['thing', 'color', '!artistic_name']
        formatters = {
            '!artistic_name': lambda obj: '{0} {1}'.format(obj.color,
                                                           obj.thing),
            'color': lambda c: c.split(' ')[1],
        }
        custom_labels = {'thing': 'name', '!artistic_name': 'artistic name'}

        fmt.print_list(self.objects(), fields, formatters, custom_labels,
                       outfile=self.outfile)
        self.assertEqual(
            ('+------+-------+-----------------+\n'
             '| name | color | artistic name   |\n'
             '+------+-------+-----------------+\n'
             '| moon | green | dark green moon |\n'
             '| sun  | blue  | bright blue sun |\n'
             '+------+-------+-----------------+\n'),
            self.outfile.getvalue()
        )

    def test_print_list_custom_field_without_formatter(self):
        fields = ['!artistic_name']

        self.assertRaises(KeyError, fmt.print_list, self.objects(), fields)

    def objects(self):
        return [
            mock.Mock(thing='sun', color='bright blue'),
            mock.Mock(thing='moon', color='dark green'),
        ]


class FormattersTest(tutils.TestCase):

    def test_attributes_formatter(self):
        """Test the attributes formatter displays the attributes correctly."""

        attributes = {
            'password': 'pass',
            'mysql_host': 'http://somewhere',
            'a thing': 'a value'
        }
        self.assertEqual(
            ("a thing=a value\nmysql_host=http://somewhere\npassword=pass\n"),
            fmt.attributes_formatter(attributes),
        )

    def test_counts_formatter(self):

        resource_link = [
            {'overcloud_role_id': 1, 'num_nodes': 10},
            {'overcloud_role_id': 2, 'num_nodes': 20}
        ]

        self.assertEqual(
            ("1=10\n2=20"),
            fmt.counts_formatter(resource_link),
        )
