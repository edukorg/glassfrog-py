import unittest

from glassfrog import models, exceptions
from tests.unit.tests_models import ModelTestMixin


class TestPolicyModel(ModelTestMixin, unittest.TestCase):
    def sample_data(self):
        item_a = {
            'id': 42,
        }
        item_b = {
            'id': 314,
        }
        return item_a, item_b

    def test_fields(self):
        data = self.sample_data()[0]
        assignment = models.Assignment(data=data)

        self.assertEqual(42, assignment.id)

    def test_invalid_field(self):
        policy = models.Policy(data={})
        with self.assertRaises(exceptions.UnexpectedDataFormat):
            policy.id

    def test_list(self):
        data = self.sample_data()
        with self.patch_get(resource='policies', data=data, many=True) as get:
            with self.assertRaises(exceptions.UnsupportedModelException):
                models.Policy.list()

        self.assertEqual(0, get.call_count)

    def test_detail(self):
        data = [self.sample_data()[0]]
        with self.patch_get(resource='policies', data=data, many=True) as get:
            policy = models.Policy.get(id=666)

        self.assertEqual(666, policy.id)
        self.assertEqual(0, get.call_count)
