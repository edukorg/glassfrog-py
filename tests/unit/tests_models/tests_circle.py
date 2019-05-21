import unittest

from glassfrog import models, exceptions
from tests.unit.tests_models import ModelTestMixin


class TestCircleModel(ModelTestMixin, unittest.TestCase):
    def sample_data(self):
        item_a = {
            'id': 42,
            'name': "Circle of Life",
            'short_name': "Life",
            'strategy': None,
            'organization_id': 1,
            'links': {
                "roles": [
                    10,
                    20,
                ],
                "policies": [
                    100,
                    200
                ],
                "domain": [
                    1000,
                    2000,
                ],
                'supported_role': 50,
            },
        }

        item_b = {
            'id': 314,
            'name': "Circle of Life",
            'short_name': "Life",
            'strategy': None,
            'organization_id': 1,
            "links": {
                "roles": [
                    30,
                    40,
                ],
                "policies": [
                    200,
                    300
                ],
                "domains": [
                    3000,
                    4000,
                ],
                'supported_role': 50,
            },
        }

        return item_a, item_b

    def test_fields(self):
        data = self.sample_data()[0]
        circle = models.Circle(data=data)

        self.assertEqual(42, circle.id)
        self.assertEqual("Circle of Life", circle.name)
        self.assertEqual("Life", circle.short_name)
        self.assertEqual(None, circle.strategy)

        self.assertTrue(isinstance(circle.organization, models.Organization))
        self.assertEqual(1, circle.organization.id)

    def test_fields_roles(self):
        data = self.sample_data()[0]
        circle = models.Circle(data=data)

        role_data = [{'id': 10}, {'id': 20}]
        with self.patch_get(resource='roles', data=role_data, many=True) as get:
            roles = list(circle.roles)

        self.assertEqual(2, len(roles))
        [role_a, role_b] = roles
        self.assertEqual(10, role_a.id)
        self.assertEqual(20, role_b.id)

        self.assertEqual(2, get.call_count)

    def test_fields_policies(self):
        data = self.sample_data()[0]
        circle = models.Circle(data=data)

        policy_data = [{'id': 100}, {'id': 200}]
        with self.patch_get(resource='policies', data=policy_data, many=True) as get:
            policies = list(circle.policies)

        self.assertEqual(2, len(policies))
        [policy_a, policy_b] = policies
        self.assertEqual(100, policy_a.id)
        self.assertEqual(200, policy_b.id)

        self.assertEqual(0, get.call_count)

    def test_fields_domains(self):
        data = self.sample_data()[0]
        circle = models.Circle(data=data)

        domain_data = [{'id': 1000}, {'id': 2000}]
        with self.patch_get(resource='domains', data=domain_data, many=True) as get:
            domains = list(circle.domains)

        self.assertEqual(2, len(domains))
        [domain_a, domain_b] = domains
        self.assertEqual(1000, domain_a.id)
        self.assertEqual(2000, domain_b.id)

        self.assertEqual(0, get.call_count)

    def test_fields_supported_role(self):
        data = self.sample_data()[0]
        circle = models.Circle(data=data)

        role_data = [{'id': 50}]
        with self.patch_get(resource='roles', data=role_data, many=True) as get:
            role = circle.supported_role

        self.assertEqual(50, role.id)

        self.assertEqual(1, get.call_count)

    def test_fields_projects(self):
        data = self.sample_data()[0]
        circle = models.Circle(data=data)

        project_data = [{'id': 666}, {'id': 999}]
        with self.patch_get(resource='projects', data=project_data, many=False) as get:
            projects = list(circle.projects)

        self.assertEqual(2, len(projects))
        [project_a, project_b] = projects
        self.assertEqual(666, project_a.id)
        self.assertEqual(999, project_b.id)

        self.assertEqual(1, get.call_count)

    def test_invalid_field(self):
        circle = models.Circle(data={})
        with self.assertRaises(exceptions.UnexpectedDataFormat):
            circle.id

    def test_list(self):
        data = self.sample_data()
        with self.patch_get(resource='circles', data=data, many=False) as get:
            circles_iter = models.Circle.list()

            circles = list(circles_iter)
            self.assertEqual(2, len(circles))

            [circle_a, circle_b] = circles
            sample_a, sample_b = self.sample_data()
            self.assertEqual(sample_a, circle_a._data)
            self.assertEqual(sample_b, circle_b._data)

        get.assert_called_once_with(resource='circles')

    def test_detail(self):
        data = [self.sample_data()[0]]
        with self.patch_get(resource='circles', data=data, many=False) as get:
            circle = models.Circle.get(id=42)

            sample = self.sample_data()[0]
            self.assertEqual(sample, circle._data)

        get.assert_called_once_with(resource='circles', id=42)
