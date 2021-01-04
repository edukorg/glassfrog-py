# pylint: disable=redefined-builtin
import os

import requests

from glassfrog import exceptions


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

        response = requests.get(
            url=url,
            headers=cls._get_headers(),
        )
        response.raise_for_status()
        return response.json()
