import json
import unittest

import httpretty
from mock import patch

from glassfrog import client, exceptions


class HTTPPrettyTestMixin:
    @property
    def request_count(self):
        return len(httpretty.httpretty.latest_requests)

    @property
    def latest_request_header(self):
        last_request = httpretty.httpretty.last_request
        return last_request.headers


class TestGlassFrogClient(HTTPPrettyTestMixin, unittest.TestCase):
    API_URL = 'https://api.glassfrog.com/api/v3'

    def patch_token(self, token='42'):
        return patch('glassfrog.client.GlassFrogClient._TOKEN', token)

    def test_token_not_set(self):
        with self.assertRaises(exceptions.TokenUndefinedException):
            client.GlassFrogClient.get(
                resource='potato',
            )

    @httpretty.activate
    def test_request_error(self):
        httpretty.register_uri(
            httpretty.GET,
            f'{self.API_URL}/potato',
            body="Find the best daily deals",
            status=404,
        )

        with self.patch_token():
            with self.assertRaises(Exception):
                client.GlassFrogClient.get(
                    resource='potato',
                )

        self.assertEqual(1, self.request_count)
        self.assertEqual('42', self.latest_request_header['X-Auth-Token'])

    @httpretty.activate
    def test_list_resource(self):
        httpretty.register_uri(
            httpretty.GET,
            f'{self.API_URL}/potato',
            body=json.dumps([{'answer': 314}]),
        )

        with self.patch_token():
            data = client.GlassFrogClient.get(
                resource='potato',
            )

        self.assertEqual(1, self.request_count)
        self.assertEqual('42', self.latest_request_header['X-Auth-Token'])
        self.assertEqual([{'answer': 314}], data)

    @httpretty.activate
    def test_detail_resource(self):
        httpretty.register_uri(
            httpretty.GET,
            f'{self.API_URL}/potato/314',
            body=json.dumps({'answer': 314}),
        )

        with self.patch_token():
            data = client.GlassFrogClient.get(
                resource='potato',
                id=314,
            )

        self.assertEqual(1, self.request_count)
        self.assertEqual('42', self.latest_request_header['X-Auth-Token'])
        self.assertEqual({'answer': 314}, data)

    @httpretty.activate
    def test_detail_from_resource(self):
        httpretty.register_uri(
            httpretty.GET,
            f'{self.API_URL}/potato/314/answers',
            body=json.dumps([{'answer': 314}]),
        )

        with self.patch_token():
            data = client.GlassFrogClient.get(
                from_resource='potato',
                id=314,
                resource='answers',
            )

        self.assertEqual(1, self.request_count)
        self.assertEqual('42', self.latest_request_header['X-Auth-Token'])
        self.assertEqual([{'answer': 314}], data)

    @httpretty.activate
    def test_detail_from_resource_without_id(self):
        with self.patch_token():
            with self.assertRaises(UnboundLocalError):
                client.GlassFrogClient.get(
                    from_resource='potato',
                    resource='answers',
                )

        self.assertEqual(0, self.request_count)
