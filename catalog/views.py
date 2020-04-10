from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from catalog.models import Category, Product, Substitute
from catalog.serializer import (
    CategorySerializer,
    ProductSerializer,
    SubstituteSerializer,
    DetailSubstituteSerializer
)
from blog.models import Comment
from blog.serializer import CommentSerializer


class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):

        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(
            queryset, self.request, view=self
        )

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class ProductPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 3


class ListCategory(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        content = {"categories": serializer.data}
        return Response(content, status=status.HTTP_200_OK)


class ListProduct(APIView, PaginationHandlerMixin):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get(self, request, format=None):
        products = Product.objects.all().order_by('name')

        cat_id = self.request.query_params.get('cat_id', None)
        if cat_id is not None:
            products = products.filter(category_id=cat_id)

        order_by = self.request.query_params.get('order_by', None)
        if order_by is not None:
            products = products.order_by(order_by)

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_paginated_response(
                self.serializer_class(page, many=True, context={'request': request}).data
            )
        else:
            serializer = self.serializer_class(products, many=True, context={'request': request})

        content = {"products": serializer.data}
        return Response(content, status=status.HTTP_200_OK)


class ListSubstitute(APIView):
    permission_classes = [AllowAny]
    serializer_class = SubstituteSerializer

    def get(self, request, id_product, format=None):
        product = get_object_or_404(Product, id=id_product)
        substitutes = product.substitutes.all()
        serializer = SubstituteSerializer(substitutes, many=True, context={'request': request})

        content = {'substitutes': serializer.data}
        return Response(content, status=status.HTTP_200_OK)


class SearchPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 6


class Search(APIView, PaginationHandlerMixin):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    pagination_class = SearchPagination

    def get(self, request, format=None):
        query = self.request.query_params.get('query', None)

        if query is None:
            products = Product.objects.all().order_by('name')
        else:
            products = Product.objects.filter(name__icontains=query).order_by('name')

        if not products.exists():
            products = Product.objects.filter(barcode=query).order_by('name')

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_paginated_response(
                self.serializer_class(page, many=True, context={'request': request}).data
            )
        else:
            serializer = self.serializer_class(products, many=True, context={'request': request})

        content = {"products": serializer.data}
        return Response(content, status=status.HTTP_200_OK)


class DetailSubstitute(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DetailSubstituteSerializer

    def get(self, request, id_substitute, format=None):
        substitute = get_object_or_404(Substitute, id=id_substitute)
        serializer = DetailSubstituteSerializer(substitute, context={'request': request})

        content = {'substitute': serializer.data}
        return Response(content, status=status.HTTP_200_OK)

    def post(self, request, id_substitute, format=None):
        substitute = get_object_or_404(Substitute, id=id_substitute)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user, substitute=substitute)
            # We return the detail of a substitute which contains all comments associated with it
            serializer = DetailSubstituteSerializer(substitute, context={'request': request})
            content = {'substitute': serializer.data}
            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
