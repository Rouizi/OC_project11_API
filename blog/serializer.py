from .models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'date_added', 'author']

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
