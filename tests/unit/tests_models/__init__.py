from mock import patch

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

    def test_fields(self):
        raise NotImplementedError()

    def test_invalid_field(self):
        raise NotImplementedError()

    def test_list(self):
        raise NotImplementedError()

    def test_detail(self):
        raise NotImplementedError()
