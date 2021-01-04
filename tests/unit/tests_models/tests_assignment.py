import unittest
from datetime import date

from glassfrog import models, exceptions
from tests.unit.tests_models import ModelTestMixin


class TestPersonModel(ModelTestMixin, unittest.TestCase):
    def sample_data(self):
        item_a = {
            "id": 1,
            "election": "1990-07-19",
            "exclude_from_meetings": False,
            "focus": '20%',
            "links": {
                "person": 10,
                "role": 100,
            }
        }

        item_b = {
            "id": 2,
            "election": None,
            "exclude_from_meetings": True,
            "focus": None,
            "links": {
                "person": 20,
                "role": 200,
            }
        }

        return item_a, item_b

    def test_fields(self):
        data = self.sample_data()[0]
        assignment = models.Assignment(data=data)

        self.assertEqual(1, assignment.id)
        self.assertEqual("20%", assignment.focus)
        self.assertEqual(False, assignment.exclude_from_meetings)

    def test_fields_person(self):
        data = self.sample_data()[0]
        assignment = models.Assignment(data=data)

        person_data = [{'id': 10}]
        with self.patch_get(resource='people', data=person_data, many=True) as get:
            person = assignment.person

        self.assertEqual(10, person.id)

        self.assertEqual(1, get.call_count)

    def test_fields_role(self):
        data = self.sample_data()[0]
        assignment = models.Assignment(data=data)

        role_data = [{'id': 100}]
        with self.patch_get(resource='roles', data=role_data, many=True) as get:
            role = assignment.role

        self.assertEqual(100, role.id)

        self.assertEqual(1, get.call_count)

    def test_fields_role_not_found(self):
        data = self.sample_data()[0]
        linked_data = {'roles': [{'id': 100}]}
        assignment = models.Assignment(data=data, linked_data=linked_data)

        with self.patch_get_error() as get:
            role = assignment.role

        self.assertEqual(100, role.id)

        self.assertEqual(1, get.call_count)

    def test_fields_election_core(self):
        data = self.sample_data()[0]
        role = models.Assignment(data=data)

        election = role.election
        self.assertEqual(date(1990, 7, 19), election)

    def test_fields_election_non_core(self):
        data = self.sample_data()[1]
        role = models.Assignment(data=data)

        election = role.election
        self.assertIsNone(election)

    def test_invalid_field(self):
        assignment = models.Assignment(data={})
        with self.assertRaises(exceptions.UnexpectedDataFormat):
            assignment.id  # pylint: disable=pointless-statement

    def test_list(self):
        data = self.sample_data()
        with self.patch_get(resource='assignments', data=data, many=False) as get:
            assignment_iter = models.Assignment.list()

            assignments = list(assignment_iter)
            self.assertEqual(2, len(assignments))

            [assignment_a, assignment_b] = assignments
            sample_a, sample_b = self.sample_data()
            self.assertEqual(sample_a, assignment_a._data)
            self.assertEqual(sample_b, assignment_b._data)

        get.assert_called_once_with(resource='assignments')

    def test_detail(self):
        data = [self.sample_data()[0]]
        with self.patch_get(resource='assignments', data=data, many=False) as get:
            assignment = models.Assignment.get(id=42)

            sample = self.sample_data()[0]
            self.assertEqual(sample, assignment._data)

        get.assert_called_once_with(resource='assignments', id=42)

    def test_not_found(self):
        with self.patch_get_error(status_code=404) as get:
            with self.assertRaises(exceptions.DoesNotExist):
                models.Assignment.get(id=666)

        self.assertEqual(1, get.call_count)
