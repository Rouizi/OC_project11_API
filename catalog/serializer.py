from .models import Category, Product, Substitute
from blog.models import Comment
from blog.serializer import CommentSerializer
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'nutri_score', 'barcode', 'picture', 'category'
        ]


class SubstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Substitute
        fields = [
            'id', 'name', 'nutri_score', 'barcode', 'url',
            'nutrition', 'picture'
        ]


class DetailSubstituteSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Substitute
        fields = [
            'id', 'name', 'nutri_score', 'barcode', 'url',
            'nutrition', 'picture', 'comments'
        ]
        read_only_fields = [
            'name', 'nutri_score', 'barcode', 'url', 'nutrition', 'picture'
        ]


class ProductSavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Substitute
        fields = [
            'id', 'name', 'nutri_score', 'picture', 'user_sub'
        ]
        read_only_fields = [
            'name', 'nutri_score', 'picture'
        ]

    def create(self, validated_data):
        substitute = validated_data.get('substitute')
        id_user = validated_data.get('user_sub')
        substitute.user_sub.add(id_user[0])
        return substitute
