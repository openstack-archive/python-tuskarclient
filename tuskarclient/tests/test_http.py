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

from tuskarclient.tests import utils as tutils

from tuskarclient.common import http
from tuskarclient import exc

import mock

fixtures = {}


class HttpClientUrlGenerationTest(tutils.TestCase):

    def test_url_generation_trailing_slash_in_base(self):
        client = http.HTTPClient('http://localhost/')
        url = client._make_connection_url('/v1/resources')
        print(client.connection_params)
        self.assertEqual(url, '/v1/resources')

    def test_url_generation_without_trailing_slash_in_base(self):
        client = http.HTTPClient('http://localhost')
        url = client._make_connection_url('/v1/resources')
        print(client.connection_params)
        self.assertEqual(url, '/v1/resources')

    def test_url_generation_prefix_slash_in_path(self):
        client = http.HTTPClient('http://localhost/')
        url = client._make_connection_url('/v1/resources')
        print(client.connection_params)
        self.assertEqual(url, '/v1/resources')

    def test_url_generation_without_prefix_slash_in_path(self):
        client = http.HTTPClient('http://localhost')
        url = client._make_connection_url('v1/resources')
        print(client.connection_params)
        self.assertEqual(url, '/v1/resources')


class HttpClientRawRequestTest(tutils.TestCase):

    def setUp(self):
        super(HttpClientRawRequestTest, self).setUp()

        client = http.HTTPClient('http://localhost')
        client._http_request = mock.MagicMock(name='_http_request')
        self.client = client

        self.call_args = {'provided_method': 'method',
                          'expected_method': 'method',
                          'provided_url': 'url',
                          'expected_url': 'url',
                          'provided_args': {
                              'headers': {},
                              'other': {}},
                          'expected_args': {
                              'headers': {
                                  'Content-Type': 'application/octet-stream'},
                              'other': {}}}

    def raw_request_calls_http_request(self,
                                       provided_method=None,
                                       provided_url=None,
                                       provided_args={},
                                       expected_method=None,
                                       expected_url=None,
                                       expected_args={}):
        self.client.raw_request(provided_method,
                                provided_url,
                                **provided_args)
        self.client._http_request.\
            assert_called_once_with(expected_url,
                                    expected_method,
                                    **expected_args)

    def test_raw_request_set_default_headers_with_empty_kwargs(self):
        args = self.call_args.copy()
        self.raw_request_calls_http_request(**args)

    def test_raw_request_set_default_headers_without_headers(self):
        args = self.call_args.copy()
        args['provided_args']['other'] = 'other_value'
        args['expected_args']['other'] = 'other_value'
        self.raw_request_calls_http_request(**args)

    def test_raw_request_set_default_headers_with_other_headers(self):
        args = self.call_args.copy()
        args['provided_args']['other'] = 'other_value'
        args['expected_args']['other'] = 'other_value'
        args['provided_args']['headers'] = {'other_header': 'other_value'}
        args['expected_args']['headers'] = {'other_header':
                                            'other_value',
                                            'Content-Type':
                                            'application/octet-stream'}
        self.raw_request_calls_http_request(**args)

    def test_raw_request_set_default_headers_with_conflicting_header(self):
        args = self.call_args.copy()
        args['provided_args']['headers'] = {'Content-Type':
                                            'conflicting_header_value'}
        args['expected_args']['headers'] = {'Content-Type':
                                            'conflicting_header_value'}
        self.raw_request_calls_http_request(**args)


class HttpClientHTTPRequestTest(tutils.TestCase):

    def setUp(self):
        super(HttpClientHTTPRequestTest, self).setUp()

        self.client = http.HTTPClient('http://localhost')
        self.call_args = {
            'provided_method': 'GET',
            'expected_method': 'GET',
            'provided_url': '/',
            'expected_url': '/',
            'provided_args': {
                'headers': {
                    'User-Agent': 'python-tuskarclient',
                },
            },
            'expected_args': {
                'headers': {
                    'Content-Type': 'application/octet-stream'},
            },
        }

        self.mock_response = mock.MagicMock()
        self.mock_response.read = lambda *args: None

        self.mock_response_2 = mock.MagicMock()
        self.mock_response_2.read = lambda *args: None

        self.mock_request = mock.MagicMock()

        self.client.get_connection = mock.MagicMock(
            return_value=self.mock_request,
        )

    def test_raw_request_status_200(self):
        self.mock_request.getresponse = lambda: self.mock_response
        self.mock_response.status = 200

        args = self.call_args.copy()
        resp, body_iter = self.client._http_request(
            args['provided_url'],
            args['provided_method'],
            **args['provided_args'])
        self.assertEqual(resp.status, 200)

    def test_raw_request_status_300(self):
        self.mock_request.getresponse = lambda: self.mock_response
        self.mock_response.status = 300

        args = self.call_args.copy()
        self.assertRaises(exc.HTTPMultipleChoices, self.client._http_request,
                          args['provided_url'], args['provided_method'],
                          **args['provided_args'])

    def test_raw_request_status_301(self):
        new_location = 'http://new_location.com'
        self.mock_response.getheader.return_value = new_location
        self.mock_response.status = 301
        self.mock_response_2.status = 200

        self.mock_request.getresponse.side_effect = [
            self.mock_response, self.mock_response_2]

        args = self.call_args.copy()

        resp, body_iter = self.client._http_request(
            args['provided_url'],
            args['provided_method'],
            **args['provided_args'])

        self.assertEqual(self.mock_request.getresponse.call_count, 2)
        self.mock_response.getheader.assert_called_called_with('location')
        self.mock_request.request.assert_called_with(
            args['provided_method'],
            new_location,
            **args['provided_args']
        )
        self.assertEqual(resp.status, 200)

    def test_raw_request_status_500(self):
        self.mock_request.getresponse = lambda: self.mock_response
        self.mock_response.status = 500

        args = self.call_args.copy()
        self.assertRaises(exc.HTTPInternalServerError,
                          self.client._http_request,
                          args['provided_url'], args['provided_method'],
                          **args['provided_args'])
