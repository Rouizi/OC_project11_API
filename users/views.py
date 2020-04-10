from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404

from catalog.serializer import ProductSavedSerializer
from catalog.models import Substitute
from users.models import User, Profile
from users.serializer import ProfileSerializer, EditProfileSerializer
from blog.models import Comment
from blog.serializer import CommentSerializer


class SaveProduct(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSavedSerializer

    def post(self, request, id_substitute, format=None):
        substitute = get_object_or_404(Substitute, id=id_substitute)
        serializer = self.serializer_class(data={'user_sub': [request.user.id]})

        if serializer.is_valid():
            serializer.save(substitute=substitute)
            data = serializer.data
            print(data)
            # Return the data without the 'user_sub' key
            content = {'substitute': {x: data[x] for x in data if x != 'user_sub'}}
            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListSavedProduct(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSavedSerializer

    def get(self, request, format=None):
        user = User.objects.filter(id=request.user.id)[0]
        substitutes = user.user_substitute.all()
        serializer = self.serializer_class(substitutes, many=True, context={'request': request})

        data = serializer.data

        # Return the data without the 'user_sub' key
        serializer_data = []
        for dic in serializer.data:
            d = {}
            for key in dic:
                if key == 'user_sub':
                    serializer_data.append(d)
                    continue
                d[key] = dic[key]
        content = {'my_favorite_substitutes': serializer_data}
        return Response(content, status=status.HTTP_200_OK)


class ProfileUser(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request):
        # If we have 'id_author_comment' in the get request it means that
        # the current user is viewing the profile of another user
        id_author_comment = self.request.query_params.get('id_author_comment', None)
        if id_author_comment is not None and id_author_comment != request.user.id:
            author_comment = get_object_or_404(User, id=id_author_comment)
            comments = Comment.objects.filter(author=author_comment)
            profile = Profile.objects.filter(user=author_comment)[0]
            profile_user = 'profile'

        else:
            comments = Comment.objects.filter(author=request.user)
            profile = Profile.objects.filter(user=request.user)[0]
            profile_user = 'profile_user_request'

        profile_serializer = self.serializer_class(profile, context={'request': request})
        comment_serializer = CommentSerializer(comments, many=True, context={'request': request})

        response = {**profile_serializer.data, **({'comments': comment_serializer.data})}
        # Like this the client side can know if the current user is viewing her
        # profile or the profile of other user so he can know when
        # displaying the link 'edit profile'
        content = {profile_user: response}
        return Response(content, status=status.HTTP_200_OK)


class EditProfile(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditProfileSerializer

    def put(self, request):
        username = request.data.get('username', request.user.username)
        profile = Profile.objects.get(user=request.user)
        bio = request.data.get('bio', profile.bio)
        data = {'user': username, 'bio': bio}
        serializer = self.serializer_class(profile, data=data)

        if serializer.is_valid():
            serializer.save()
            content = {'profile': serializer.data}
            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
