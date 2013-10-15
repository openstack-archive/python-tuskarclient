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

import io
import mock

import tuskarclient.common.formatting as fmt
import tuskarclient.tests.utils as tutils


class PrintTest(tutils.TestCase):

    def setUp(self):
        super(PrintTest, self).setUp()
        self.outfile = io.StringIO()

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

    def test_attr_formatter_plain(self):
        obj = mock.Mock()
        obj.foo = 'bar'
        foo_formatter = fmt.attr_proxy('foo')
        self.assertEqual('bar', foo_formatter(obj))

    def test_attr_formatter_chained(self):
        obj = mock.Mock()
        obj.letters = ['a', 'b', 'c']
        letters_formatter = fmt.attr_proxy('letters', len)
        self.assertEqual(3, letters_formatter(obj))

    def test_capacities_formatter(self):
        capacities = [
            {'name': 'memory', 'value': '1024', 'unit': 'MB'},
            {'name': 'cpu', 'value': '2', 'unit': 'CPU'},
        ]
        self.assertEqual(
            ('cpu: 2 CPU\n'
             'memory: 1024 MB'),
            fmt.capacities_formatter(capacities),
        )

    def test_links_formatter(self):
        links = [
            {'rel': 'self', 'href': 'http://self-url'},
            {'rel': 'parent', 'href': 'http://parent-url'},
        ]
        self.assertEqual(
            ('parent: http://parent-url\n'
             'self: http://self-url'),
            fmt.links_formatter(links),
        )

    def test_resource_links_formatter(self):
        resource_links = [
            {'id': 3, 'links': [{'rel': 'self', 'href': 'http://three'}]},
            {'id': 5, 'links': [{'rel': 'self', 'href': 'http://five'}]},
        ]
        self.assertEqual(
            ('3: http://three\n'
             '5: http://five'),
            fmt.resource_links_formatter(resource_links),
        )

    def test_resource_link_formatter(self):
        resource_link = {
            'id': 3,
            'links': [{'rel': 'self', 'href': 'http://three'}]
        }
        self.assertEqual(
            ('3: http://three'),
            fmt.resource_link_formatter(resource_link),
        )
