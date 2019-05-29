import unittest

from glassfrog import models, exceptions
from tests.unit.tests_models import ModelTestMixin


class TestPersonModel(ModelTestMixin, unittest.TestCase):
    def sample_data(self):
        item_a = {
            "id": 42,
            "name": "Chuck Norris",
            "email": "chuck@norris.com",
            "links": {
                "circles": [
                    100,
                    200,
                ],
                "organization_ids": [
                    1,
                ]
            }
        }

        item_b = {
            "id": 314,
            "name": "Justin Beaver",
            "email": "justin@beaver.com",
            "links": {
                "circles": [
                    300,
                    400,
                ],
                "organization_ids": [
                    1,
                ]
            }
        }

        return item_a, item_b

    def test_fields(self):
        data = self.sample_data()[0]
        person = models.Person(data=data)

        self.assertEqual(42, person.id)
        self.assertEqual("Chuck Norris", person.name)
        self.assertEqual("chuck@norris.com", person.email)

    def test_fields_organizations(self):
        data = self.sample_data()[0]
        person = models.Person(data=data)

        organization_data = [{'id': 1}]
        with self.patch_get(resource='organizations', data=organization_data, many=True) as get:
            organizations = list(person.organizations)

        self.assertEqual(1, len(organizations))
        [organization] = organizations
        self.assertEqual(1, organization.id)

        self.assertEqual(0, get.call_count)

    def test_fields_circles(self):
        data = self.sample_data()[0]
        person = models.Person(data=data)

        circle_data = [{'id': 100}, {'id': 200}]
        with self.patch_get(resource='circles', data=circle_data, many=True) as get:
            circles = list(person.circles)

        self.assertEqual(2, len(circles))
        [circle_a, circle_b] = circles
        self.assertEqual(100, circle_a.id)
        self.assertEqual(200, circle_b.id)

        self.assertEqual(2, get.call_count)

    def test_fields_assignments(self):
        data = self.sample_data()[0]
        person = models.Person(data=data)

        assign_data = [{'id': 10000}, {'id': 20000}]
        with self.patch_get(resource='assignments', data=assign_data, many=False) as get:
            assignments = list(person.assignments)

        self.assertEqual(2, len(assignments))
        [assignment_a, assignment_b] = assignments
        self.assertEqual(10000, assignment_a.id)
        self.assertEqual(20000, assignment_b.id)

        self.assertEqual(1, get.call_count)

    def test_invalid_field(self):
        person = models.Person(data={})
        with self.assertRaises(exceptions.UnexpectedDataFormat):
            person.id

    def test_list(self):
        data = self.sample_data()
        with self.patch_get(resource='people', data=data, many=False) as get:
            people_iter = models.Person.list()

            people = list(people_iter)
            self.assertEqual(2, len(people))

            [person_a, person_b] = people
            sample_a, sample_b = self.sample_data()
            self.assertEqual(sample_a, person_a._data)
            self.assertEqual(sample_b, person_b._data)

        get.assert_called_once_with(resource='people')

    def test_detail(self):
        data = [self.sample_data()[0]]
        with self.patch_get(resource='people', data=data, many=False) as get:
            person = models.Person.get(id=42)

            sample = self.sample_data()[0]
            self.assertEqual(sample, person._data)

        get.assert_called_once_with(resource='people', id=42)

    def test_not_found(self):
        with self.patch_get_error(status_code=404) as get:
            with self.assertRaises(exceptions.DoesNotExist):
                models.Person.get(id=666)

        self.assertEqual(1, get.call_count)
