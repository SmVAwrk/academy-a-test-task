from django.test import TestCase
from rest_framework.exceptions import ValidationError

from storage_app.models import Resource
from storage_app.services import id_validation


class IDValidationTestCase(TestCase):

    def test_ok(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')

        resource_obj = id_validation(res_1.id)

        self.assertEqual(resource_obj, res_1)

    def test_empty_id(self):
        with self.assertRaises(ValidationError):
            id_validation(None)

    def test_not_valid_type(self):
        with self.assertRaises(ValidationError):
            id_validation(dict())

    def test_not_valid_id(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')

        with self.assertRaises(ValidationError):
            id_validation(res_1.id + 100)
