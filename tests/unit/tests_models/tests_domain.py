import unittest

from glassfrog import models
from tests.unit.tests_models import UnsupportedModelTestMixin


class TestDomainModel(UnsupportedModelTestMixin, unittest.TestCase):
    model_klass = models.Domain
    resource_key = 'domains'
