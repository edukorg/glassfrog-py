from mock import patch
from requests import HTTPError, Response

from tests.unit.tests_client import HTTPPrettyTestMixin


class ModelTestMixin(HTTPPrettyTestMixin):
    API_URL = 'https://api.glassfrog.com'

    def patch_get(self, resource, data, many=False):
        if many:
            kwargs = {
                'side_effect': [
                    {resource: [item]}
                    for item in data
                ]
            }
        else:
            kwargs = {
                'return_value': {resource: data}
            }
        return patch('glassfrog.client.GlassFrogClient.get', **kwargs)

    def patch_get_error(self, content=None, status_code=404):
        response = Response()
        response.status_code = status_code
        response._content = content
        error = HTTPError(response=response)
        return patch('glassfrog.client.GlassFrogClient.get', side_effect=error)

    def test_fields(self):
        raise NotImplementedError()

    def test_invalid_field(self):
        raise NotImplementedError()

    def test_list(self):
        raise NotImplementedError()

    def test_detail(self):
        raise NotImplementedError()

    def test_not_found(self):
        raise NotImplementedError()
