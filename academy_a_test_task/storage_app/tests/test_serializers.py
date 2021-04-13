from django.test import TestCase
from rest_framework.exceptions import ValidationError

from storage_app.models import Resource
from storage_app.serializers import ResourceSerializer


class ResourceSerializerTestCase(TestCase):

    def test_ok(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')
        res_2 = Resource.objects.create(title='res_2', amount=200, unit='liter', price=10, date='2021-03-21')

        expected_data = [
            {
                "title": "res_1",
                "id": res_1.id,
                "amount": 100,
                "unit": "kg",
                "price": 15,
                "cost": res_1.amount * res_1.price,
                "date": "2020-03-21"
            },
            {
                "title": "res_2",
                "id": res_2.id,
                "amount": 200,
                "unit": "liter",
                "price": 10,
                "cost": res_2.amount * res_2.price,
                "date": "2021-03-21"
            }
        ]

        serializer = ResourceSerializer([res_1, res_2], many=True)

        self.assertEqual(serializer.data, expected_data)

    def test_read_only_fields(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')

        input_data = {
            "title": "res_1",
            "id": 10,
            "amount": 100,
            "unit": "liter",
            "price": 15,
            "cost": 100000,
            "date": "2020-03-21"
        }

        serializer = ResourceSerializer(instance=res_1, data=input_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.assertNotEqual(res_1.id, 10)
        self.assertEqual(res_1.amount * res_1.price, serializer.data['cost'])
        self.assertEqual(res_1.unit, "liter")

    def test_amount_field_validation(self):
        input_data = {
            "title": "res_1",
            "amount": -100,
            "unit": "liter",
            "price": 10,
            "date": "2020-03-21"
        }

        serializer = ResourceSerializer(data=input_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_price_field_validation(self):
        input_data = {
            "title": "res_1",
            "amount": 100,
            "unit": "liter",
            "price": -1,
            "date": "2020-03-21"
        }

        serializer = ResourceSerializer(data=input_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

