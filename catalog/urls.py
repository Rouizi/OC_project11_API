from django.urls import path
from catalog.views import (
    ListCategory, ListProduct, ListSubstitute, Search, DetailSubstitute
)

urlpatterns = [
    path('list-categories/', ListCategory.as_view(), name='list-categories'),
    path('list-products/', ListProduct.as_view(), name='list-products'),
    path('list-substitutes/<id_product>', ListSubstitute.as_view(), name='list-substitutes'),
    path('substitute/<id_substitute>', DetailSubstitute.as_view(), name='substitute'),
    path('search/', Search.as_view(), name='search'),
]
