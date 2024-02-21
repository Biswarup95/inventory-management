from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Inventory

class InventoryAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.inventory1 = Inventory.objects.create(product_id='123', product_name='Product 1', vendor='Vendor A', mrp=10.99, batch_num='B001', batch_date='2023-01-01', quantity=100, status='Pending', approved=False)

    def test_fetch_inventory_records(self):
        url = reverse('inventory-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_add_inventory_record(self):
        url = reverse('inventory-list-create')
        data = {'product_id': '456', 'product_name': 'Product 2', 'vendor': 'Vendor B', 'mrp': 20.99, 'batch_num': 'B002', 'batch_date': '2023-02-01', 'quantity': 200, 'status': 'Pending', 'approved': False}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_approve_inventory_record(self):
        url = reverse('inventory-retrieve-update-delete', kwargs={'pk': self.inventory1.id})
        data = {'status': 'Approved', 'approved': True}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['approved'])
