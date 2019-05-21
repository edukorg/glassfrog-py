import unittest
from datetime import date

from glassfrog import models, exceptions
from tests.unit.tests_models import ModelTestMixin


class TestRoleModel(ModelTestMixin, unittest.TestCase):
    def sample_data(self):
        item_a = {
            'id': 42,
            'name': "Circle of Life",
            'short_name': "Life",
            'purpose': "Answer the question",
            'strategy': None,
            'organization_id': 1,
            'is_core': True,
            'elected_until': '1990-07-19',
            'links': {
                "circle": 10000,
                "supporting_circle": 30000,
                "accountabilities": [
                    10,
                    20,
                ],
                "policies": [
                    100,
                    200
                ],
                "domains": [
                    1000,
                    2000,
                ],
                "people": [
                    100000,
                    200000,
                ],
            },
        }

        item_b = {
            'id': 314,
            'name': "Circle of Life",
            'short_name': "Life",
            'purpose': "Answer the question",
            'strategy': None,
            'organization_id': 1,
            'is_core': False,
            "links": {
                "circle": 20000,
                "supporting_circle": 40000,
                "accountabilities": [
                    30,
                    40,
                ],
                "policies": [
                    300,
                    400
                ],
                "domains": [
                    3000,
                    4000,
                ],
                "people": [
                    300000,
                    400000,
                ],
            },
        }

        return item_a, item_b

    def test_fields(self):
        data = self.sample_data()[0]
        role = models.Role(data=data)

        self.assertEqual(42, role.id)
        self.assertEqual("Circle of Life", role.name)
        self.assertEqual("Life", role.short_name)
        self.assertEqual("Answer the question", role.purpose)
        self.assertEqual(True, role.is_core)

        self.assertTrue(isinstance(role.organization, models.Organization))
        self.assertEqual(1, role.organization.id)

    def test_fields_circle(self):
        data = self.sample_data()[0]
        role = models.Role(data=data)

        circle_data = [{'id': 10}]
        with self.patch_get(resource='circles', data=circle_data, many=True) as get:
            circle = role.circle

        self.assertEqual(10, circle.id)

        self.assertEqual(1, get.call_count)

    def test_fields_accontabilities(self):
        data = self.sample_data()[0]
        role = models.Role(data=data)

        account_data = [{'id': 10}, {'id': 20}]
        with self.patch_get(resource='accountabilities', data=account_data, many=True) as get:
            accountabilities = list(role.accountabilities)

        self.assertEqual(2, len(accountabilities))
        [accountabilities_a, accountabilities_b] = accountabilities
        self.assertEqual(10, accountabilities_a.id)
        self.assertEqual(20, accountabilities_b.id)

        self.assertEqual(0, get.call_count)

    def test_fields_domains(self):
        data = self.sample_data()[0]
        role = models.Role(data=data)

        domain_data = [{'id': 1000}, {'id': 2000}]
        with self.patch_get(resource='domains', data=domain_data, many=True) as get:
            domains = list(role.domains)

        self.assertEqual(2, len(domains))
        [domain_a, domain_b] = domains
        self.assertEqual(1000, domain_a.id)
        self.assertEqual(2000, domain_b.id)

        self.assertEqual(0, get.call_count)

    def test_fields_supporting_circle(self):
        data = self.sample_data()[0]
        role = models.Role(data=data)

        circle_data = [{'id': 50}]
        with self.patch_get(resource='circles', data=circle_data, many=True) as get:
            role = role.supporting_circle

        self.assertEqual(50, role.id)

        self.assertEqual(1, get.call_count)

    def test_fields_people(self):
        data = self.sample_data()[0]
        role = models.Role(data=data)

        people_data = [{'id': 100000}, {'id': 200000}]
        with self.patch_get(resource='people', data=people_data, many=True) as get:
            people = list(role.people)

        self.assertEqual(2, len(people))
        [person_a, person_b] = people
        self.assertEqual(100000, person_a.id)
        self.assertEqual(200000, person_b.id)

        self.assertEqual(2, get.call_count)

    def test_fields_assignments(self):
        data = self.sample_data()[0]
        role = models.Role(data=data)

        assign_data = [{'id': 666}, {'id': 999}]
        with self.patch_get(resource='assignments', data=assign_data, many=False) as get:
            assignments = list(role.assignments)

        self.assertEqual(2, len(assignments))
        [assignment_a, assignment_b] = assignments
        self.assertEqual(666, assignment_a.id)
        self.assertEqual(999, assignment_b.id)

        self.assertEqual(1, get.call_count)

    def test_fields_elected_core(self):
        data = self.sample_data()[0]
        role = models.Role(data=data)

        election = role.elected_until
        self.assertEqual(date(1990, 7, 19), election)

    def test_fields_elected_non_core(self):
        data = self.sample_data()[1]
        role = models.Role(data=data)

        election = role.elected_until
        self.assertIsNone(election)

    def test_invalid_field(self):
        role = models.Role(data={})
        with self.assertRaises(exceptions.UnexpectedDataFormat):
            role.id

    def test_list(self):
        data = self.sample_data()
        with self.patch_get(resource='roles', data=data, many=False) as get:
            roles_iter = models.Role.list()

            roles = list(roles_iter)
            self.assertEqual(2, len(roles))

            [role_a, role_b] = roles
            sample_a, sample_b = self.sample_data()
            self.assertEqual(sample_a, role_a._data)
            self.assertEqual(sample_b, role_b._data)

        get.assert_called_once_with(resource='roles')

    def test_detail(self):
        data = [self.sample_data()[0]]
        with self.patch_get(resource='roles', data=data, many=False) as get:
            role = models.Role.get(id=42)

            sample = self.sample_data()[0]
            self.assertEqual(sample, role._data)

        get.assert_called_once_with(resource='roles', id=42)
