import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from storage_app.models import Resource
from storage_app.serializers import ResourceSerializer


class GetTotalCoastViewTestCase(APITestCase):

    def test_ok(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')
        res_2 = Resource.objects.create(title='res_2', amount=200, unit='liter', price=10, date='2021-03-21')
        res_3 = Resource.objects.create(title='res_3', amount=300, unit='m', price=5, date='2021-03-21')

        expected_data = {
            'total_cost': round(res_1.amount * res_1.price + res_2.amount * res_2.price + res_3.amount * res_3.price, 3)
        }

        url = reverse('total_cost')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_ok_with_round(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15.125, date='2020-03-21')
        res_2 = Resource.objects.create(title='res_2', amount=200, unit='liter', price=10.11, date='2021-03-21')

        expected_data = {
            'total_cost': round(res_1.amount * res_1.price + res_2.amount * res_2.price, 2)
        }

        url = reverse('total_cost')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_ok_with_no_data(self):
        expected_data = {
            'total_cost': 0
        }

        url = reverse('total_cost')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class ResourceAPIViewTestCase(APITestCase):

    def test_get(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')
        res_2 = Resource.objects.create(title='res_2', amount=200, unit='liter', price=10, date='2021-03-21')
        res_3 = Resource.objects.create(title='res_3', amount=300, unit='m', price=5, date='2021-03-21')

        serializer = ResourceSerializer([res_1, res_2, res_3], many=True)

        url = reverse('resources')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['resources'], serializer.data)
        self.assertEqual(response.data['total_count'], 3)

    def test_post_json(self):
        input_data = {
            "title": "res_0",
            "amount": 1000,
            "unit": "kg",
            "price": 12,
            "date": "2022-02-12"
        }
        input_data_json = json.dumps(input_data)

        url = reverse('resources')
        response = self.client.post(url, data=input_data_json, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resource.objects.count(), 1)

    def test_post_form_data(self):
        input_data = {
            "title": "res_0",
            "amount": 1000,
            "unit": "kg",
            "price": 12,
            "date": "2022-02-12"
        }

        url = reverse('resources')
        response = self.client.post(url, data=input_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resource.objects.count(), 1)

    def test_post_without_req_field(self):
        input_data = {
            "amount": 1000,
            "unit": "kg",
            "price": 12,
            "date": "2022-02-12"
        }

        url = reverse('resources')
        response = self.client.post(url, data=input_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_not_valid_field(self):
        input_data = {
            "title": "res_0",
            "amount": -10,
            "unit": "kg",
            "price": 10,
            "date": "2022-02-12"
        }

        url = reverse('resources')
        response = self.client.post(url, data=input_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')
        input_data = {
            "id": res_1.id,
            "title": "res_1",
            "amount": 100,
            "unit": "kg",
            "price": 9,
            "date": "2020-03-21"
        }

        url = reverse('resources')
        response = self.client.put(url, data=input_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], 9)

    def test_put_without_id(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')
        input_data = {
            "title": "res_1",
            "amount": 100,
            "unit": "kg",
            "price": 9,
            "date": "2020-03-21"
        }

        url = reverse('resources')
        response = self.client.put(url, data=input_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_without_field(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')
        input_data = {
            "id": res_1.id,
            "amount": 100,
            "unit": "kg",
            "price": 9,
            "date": "2020-03-21"
        }

        url = reverse('resources')
        response = self.client.put(url, data=input_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_with_not_valid_field(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')
        input_data = {
            "id": res_1.id,
            "title": "res_1",
            "amount": 100,
            "unit": "kg",
            "price": -10,
            "date": "2020-03-21"
        }

        url = reverse('resources')
        response = self.client.put(url, data=input_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')
        input_data = {
            "id": res_1.id,
            "title": "res_0",
        }

        url = reverse('resources')
        response = self.client.patch(url, data=input_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "res_0")

    def test_patch_without_id(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')
        input_data = {
            "title": "res_0"
        }

        url = reverse('resources')
        response = self.client.patch(url, data=input_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_with_not_valid_field(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')
        input_data = {
            "id": res_1.id,
            "price": -10,
            "date": "2022-02-13"
        }

        url = reverse('resources')
        response = self.client.patch(url, data=input_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')
        input_data = {
            "id": res_1.id
        }

        url = reverse('resources')
        response = self.client.delete(url, data=input_data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Resource.objects.count(), 0)

    def test_delete_without_id(self):
        res_1 = Resource.objects.create(title='res_1', amount=100, unit='kg', price=15, date='2020-03-21')
        input_data = {
            "title": "res_1"
        }

        url = reverse('resources')
        response = self.client.delete(url, data=input_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
