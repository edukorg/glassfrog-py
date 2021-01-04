import unittest

from glassfrog import models
from tests.unit.tests_models import UnsupportedModelTestMixin


class TestAccountabilityModel(UnsupportedModelTestMixin, unittest.TestCase):
    model_klass = models.Accountability
    resource_key = 'accountabilities'
