import unittest
from datetime import datetime, timezone

from glassfrog import models, exceptions
from tests.unit.tests_models import ModelTestMixin


class TestProjectModel(ModelTestMixin, unittest.TestCase):
    def sample_data(self):
        item_a = {
            "id": 42,
            "description": "Please, fill up the experts in Hollywood",
            "status": "Waiting",
            "waiting_on_who": "T-Rex",
            "waiting_on_what": "Extend its arms",
            "link": 'http://pudim.com.br/pudim.jpg',
            "value": 4,
            "effort": 10,
            "roi": 0.6,
            "private_to_circle": True,
            "created_at": "2016-11-06T18:51:12Z",
            "archived_at": "2019-11-06T18:51:12Z",
            "type": "project",
            "links": {
                "role": 100,
                "person": 10,
                "circle": 1,
            }
        }
        item_b = {
            "id": 666,
            "description": "I want you to do this for me",
            "status": "Current",
            "link": 'http://pudim.com.br/pudim.jpg',
            "value": None,
            "effort": None,
            "roi": None,
            "private_to_circle": False,
            "created_at": "2016-11-06T18:51:12Z",
            "archived_at": None,
            "type": "project",
            "links": {
                "role": 100,
                "person": 10,
                "circle": 1,
            }
        }
        return item_a, item_b

    def test_fields(self):
        data = self.sample_data()[0]
        project = models.Project(data=data)

        self.assertEqual(42, project.id)
        self.assertEqual("Please, fill up the experts in Hollywood", project.description)
        self.assertEqual("Waiting", project.status)
        self.assertEqual("Extend its arms", project.waiting_on_what)
        self.assertEqual("T-Rex", project.waiting_on_who)
        self.assertEqual(True, project.private_to_circle)

        expected_date = datetime(2016, 11, 6, 18, 51, 12, tzinfo=timezone.utc)
        self.assertEqual(expected_date, project.created_at)

        expected_date = datetime(2019, 11, 6, 18, 51, 12, tzinfo=timezone.utc)
        self.assertEqual(expected_date, project.archived_at)

    def test_fields_empty(self):
        data = self.sample_data()[1]
        project = models.Project(data=data)

        self.assertEqual(666, project.id)
        self.assertEqual("I want you to do this for me", project.description)
        self.assertEqual("Current", project.status)
        self.assertEqual(None, project.waiting_on_what)
        self.assertEqual(None, project.waiting_on_who)
        self.assertEqual(False, project.private_to_circle)

        expected_date = datetime(2016, 11, 6, 18, 51, 12, tzinfo=timezone.utc)
        self.assertEqual(expected_date, project.created_at)

        self.assertEqual(None, project.archived_at)

    def test_fields_person(self):
        data = self.sample_data()[0]
        project = models.Project(data=data)

        person_data = [{'id': 10}]
        with self.patch_get(resource='people', data=person_data, many=True) as get:
            person = project.person

        self.assertEqual(10, person.id)

        self.assertEqual(1, get.call_count)

    def test_fields_role(self):
        data = self.sample_data()[0]
        project = models.Project(data=data)

        role_data = [{'id': 100}]
        with self.patch_get(resource='roles', data=role_data, many=True) as get:
            role = project.role

        self.assertEqual(100, role.id)

        self.assertEqual(1, get.call_count)

    def test_fields_circle(self):
        data = self.sample_data()[0]
        project = models.Project(data=data)

        circle_data = [{'id': 1}]
        with self.patch_get(resource='circles', data=circle_data, many=True) as get:
            circle = project.circle

        self.assertEqual(1, circle.id)

        self.assertEqual(1, get.call_count)

    def test_invalid_field(self):
        project = models.Project(data={})
        with self.assertRaises(exceptions.UnexpectedDataFormat):
            project.id  # pylint: disable=pointless-statement

    def test_list(self):
        data = self.sample_data()
        with self.patch_get(resource='projects', data=data, many=True) as get:
            with self.assertRaises(exceptions.UnsupportedModelException):
                models.Project.list()

        self.assertEqual(0, get.call_count)

    def test_detail(self):
        data = [self.sample_data()[0]]
        with self.patch_get(resource='projects', data=data, many=True) as get:
            with self.assertRaises(exceptions.UnsupportedModelException):
                models.Project.get(id=666)

        self.assertEqual(0, get.call_count)

    def test_not_found(self):
        with self.patch_get_error(status_code=404) as get:
            with self.assertRaises(exceptions.UnsupportedModelException):
                models.Project.get(id=666)

        self.assertEqual(0, get.call_count)
