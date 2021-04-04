# pylint: disable=redefined-builtin
import os

import requests
from retrying import retry

from glassfrog import exceptions


def retry_if_conn_error(exception):
    return isinstance(exception, ConnectionError) or isinstance(exception, requests.HTTPError)


class GlassFrogClient:
    _URL = 'https://api.glassfrog.com/api/v3'
    _TOKEN = os.environ.get('GLASSFROG_API_TOKEN')

    @classmethod
    def _get_headers(cls):
        if not cls._TOKEN:
            raise exceptions.TokenUndefinedException()

        return {
            "X-Auth-Token": cls._TOKEN,
            "Content-Type": "application/json",
        }

    @classmethod
    def get(cls, resource, id=None, from_resource=None):
        if from_resource:
            if not id:
                raise UnboundLocalError()
            url = f'{cls._URL}/{from_resource}/{id}/{resource}'
        elif id:
            url = f'{cls._URL}/{resource}/{id}'
        else:
            url = f'{cls._URL}/{resource}'

        with retry(stop_max_attempt_number=3, retry_on_exception=retry_if_conn_error):
            response = requests.get(
                url=url,
                headers=cls._get_headers(),
            )
        response.raise_for_status()
        return response.json()
