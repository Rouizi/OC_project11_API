from rest_framework import serializers
from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_login']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['bio', 'user']


class EditProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ['bio', 'user']

    def update(self, instance, validated_data):
        username = validated_data.get('user').get('username')
        user = User.objects.get(username=instance.user.username)
        if username != instance.user.username:
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    {'user': ['A user with that username already exists.']}
                )
            user.username = username
            user.save()

        instance.bio = validated_data.get('bio')
        instance.user = user
        instance.save()
        return instance
