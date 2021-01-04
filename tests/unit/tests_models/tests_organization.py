import unittest

from glassfrog import models
from tests.unit.tests_models import UnsupportedModelTestMixin


class TestOrganizationModel(UnsupportedModelTestMixin, unittest.TestCase):
    model_klass = models.Organization
    resource_key = 'organizations'
