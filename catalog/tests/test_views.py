from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.renderers import JSONRenderer

from catalog.models import Category, Product, Substitute
from catalog.serializer import (
    CategorySerializer, ProductSerializer, SubstituteSerializer,
    DetailSubstituteSerializer, ProductSavedSerializer
)


class ListCategoryAPIViewTest(APITestCase):

    def test_list_category(self):
        self.assertEqual(Category.objects.count(), 0)

        Category.objects.create(name='category1')
        url = reverse('catalog:list-categories')
        response = self.client.get(url, format='json')

        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        content = {"categories": serializer.data}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(response.data, content)
