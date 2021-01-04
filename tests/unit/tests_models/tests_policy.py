import unittest

from glassfrog import models
from tests.unit.tests_models import UnsupportedModelTestMixin


class TestPolicyModel(UnsupportedModelTestMixin, unittest.TestCase):
    model_klass = models.Policy
    resource_key = 'policies'
