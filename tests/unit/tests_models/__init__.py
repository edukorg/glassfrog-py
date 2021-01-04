from abc import ABC
from unittest.mock import patch

from requests import HTTPError, Response

from glassfrog import exceptions
from tests.unit.tests_client import HTTPPrettyTestMixin


class ModelTestMixin(HTTPPrettyTestMixin, ABC):
    API_URL = 'https://api.glassfrog.com'
    model_klass = None
    resource_key = None

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

    def sample_data(self):
        raise NotImplementedError()

    def test_fields(self):
        sample = self.sample_data()[0]
        obj = self.model_klass(data=sample)  # pylint: disable=not-callable
        self.assertEqual(sample['id'], obj.id)

    def test_invalid_field(self):
        obj = self.model_klass(data={})  # pylint: disable=not-callable
        with self.assertRaises(exceptions.UnexpectedDataFormat):
            obj.id  # pylint: disable=pointless-statement

    def test_list(self):
        data = self.sample_data()
        with self.patch_get(resource=self.resource_key, data=data, many=False) as get:
            obj_iter = self.model_klass.list()

            all_objects = list(obj_iter)

            expected_amount = len(data)
            self.assertEqual(expected_amount, len(all_objects))

            for obj, expected_obj in zip(all_objects, data):
                self.assertEqual(expected_obj, obj._data)

        get.assert_called_once_with(resource=self.resource_key)

    def test_detail(self):
        sample = self.sample_data()[0]
        pk = sample['id']

        with self.patch_get(resource=self.resource_key, data=[sample], many=False) as get:
            obj = self.model_klass.get(id=pk)
            self.assertEqual(sample, obj._data)

        get.assert_called_once_with(resource=self.resource_key, id=pk)

    def test_not_found(self):
        with self.patch_get_error(status_code=404) as get:
            with self.assertRaises(exceptions.DoesNotExist):
                self.model_klass.get(id=666)

        self.assertEqual(1, get.call_count)

    def test_serialize(self):
        sample = self.sample_data()[0]
        obj = self.model_klass(data=sample)  # pylint: disable=not-callable

        serialized = obj.serialize()
        new_obj = self.model_klass.deserialize(**serialized)

        self.assertEqual(obj._data, new_obj._data)
        self.assertEqual(obj._linked_data, new_obj._linked_data)


class UnsupportedModelTestMixin(ModelTestMixin, ABC):
    def sample_data(self):
        item_a = {
            'id': 42,
        }
        item_b = {
            'id': 314,
        }
        return item_a, item_b

    def test_list(self):
        data = self.sample_data()
        with self.patch_get(resource=self.resource_key, data=data, many=True) as get:
            with self.assertRaises(exceptions.UnsupportedModelException):
                self.model_klass.list()

        self.assertEqual(0, get.call_count)

    def test_detail(self):
        sample = self.sample_data()[0]
        pk = sample['id']
        with self.patch_get(resource=self.resource_key, data=[sample], many=True) as get:
            with self.assertRaises(exceptions.UnsupportedModelException):
                self.model_klass.get(id=pk)

        self.assertEqual(0, get.call_count)

    def test_not_found(self):
        with self.patch_get_error(status_code=404) as get:
            with self.assertRaises(exceptions.UnsupportedModelException):
                self.model_klass.get(id=666)

        self.assertEqual(0, get.call_count)
