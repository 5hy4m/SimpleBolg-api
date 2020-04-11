from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_201_CREATED,HTTP_204_NO_CONTENT
from .models import *
import json
from django.core import serializers as serial # this is Django serilizer
from .serializers import *

User = get_user_model()


# 'request.user' will be a Django 'User' instance.
# 'request.auth' will be a 'rest_framework.authtoken.models.Token' instance.

# Create your views here.
class CreateUserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer  

class Logout(APIView):
    permission_classes = (IsAuthenticated)
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=HTTP_200_OK)

class PostsViewset(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated)
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer

        # To get the Comments of a specific Post
    @action(methods=['get'], detail=True,)
    def comments(self,request,pk=None):
        comments_json = json.loads(serial.serialize('json',CommentModel.objects.filter(post = pk)))
        comments = []
        for comment in comments_json:
            # print(comment)
            user = User.objects.filter(id=comment['fields']['user'])
            comment['fields']['comment_id'] = comment['pk']
            comment['fields']['username'] = user[0].username
            comments.append(comment['fields'])
        return Response(comments,status =200)

    def create(self, request, *args, **kwargs):
        user_obj = User.objects.filter(username=request.data['user'])
        request.data['user'] = user_obj[0].id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(user_obj[0].username)
        json = serializer.data
        json['username'] = user_obj[0].username
        return Response(json, status=HTTP_201_CREATED, headers=headers)

    def destroy(self, request,pk=None):
        post = PostModel.objects.filter(Q(user = request.user) & Q(post_id = pk))
        self.perform_destroy(post)
        return Response({"post":pk})

    def list(self, request):
        # print("POST")
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        for data in serializer.data:
            user = User.objects.filter(id=data['user'])
            data['username'] = user[0].username
        return Response(reversed(serializer.data))

class LikeViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = LikeModel.objects.all()
    serializer_class = LikeSerializer

    @action(methods=['post'], detail=True,)
    def Is_already_liked(self,request,pk=None):
        print(request.data,"   :  ",request.user,"  :  ",request.data['post'])
        like_qs = LikeModel.objects.filter(post=request.data['post'])
        # print(like_qs)
        for i in like_qs:
            # print(i.user)
            if request.user == i.user:
                # print(True)
                return Response(True)
        return Response(False)

    def create(self, request, *args, **kwargs):
        request.data['user'] = User.objects.get(username=request.user).id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = PostModel.objects.get(post_id=request.data['post']) # incrementing no of comments
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def destroy(self, request,pk=None):
        post = PostModel.objects.get(post_id=pk) # incrementing no of comments
        post_id = post.post_id
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        like = LikeModel.objects.filter(Q(user = request.user) & Q(post = pk))
        self.perform_destroy(like)
        return Response({"post":post_id})

class CommentViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer

    @action(methods=['get'], detail=True,)
    def replies(self,request,pk=None):
        replies_json = json.loads(serial.serialize('json',ReplyModel.objects.filter(comment = pk)))
        replies = []
        for reply in replies_json:
            # print(comment)
            user = User.objects.filter(id=reply['fields']['user'])
            reply['fields']['username'] = user[0].username
            reply['fields']['reply_id'] = reply['pk']
            replies.append(reply['fields'])
        return Response(replies,status =200)

    def create(self, request, *args, **kwargs):
        user_obj = User.objects.filter(username=request.data['user'])
        request.data['user'] = user_obj[0].id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = PostModel.objects.get(post_id=request.data['post']) # incrementing no of comments
        post.no_of_comments = post.no_of_comments + 1
        post.save()
        # print(PostModel.objects.filter(post_id=request.data['post'])[0])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def destroy(self, request,pk=None):
        print("POST",request.data)
        cmt = CommentModel.objects.filter(Q(user = request.user) & Q(comment_id = pk))
        post = PostModel.objects.get(post_id=request.data['post']) # incrementing no of comments
        post.no_of_comments = post.no_of_comments - 1
        post.save()
        self.perform_destroy(cmt)

        return Response({"comment":pk})

    def list(self, request):
        print(request.auth)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        for data in serializer.data:
            print(data)
            user = User.objects.filter(id=data['user'])
            data['username'] = user[0].username
        return Response(reversed(serializer.data))

class ReplyViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ReplyModel.objects.all()
    serializer_class = ReplySerializer

    def create(self, request, *args, **kwargs):
        user_obj = User.objects.filter(username=request.data['user'])
        request.data['user'] = user_obj[0].id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def destroy(self, request,pk=None):
        print("POST",request.data)
        reply = ReplyModel.objects.filter(Q(user = request.user) & Q(reply_id = pk))
        self.perform_destroy(reply)
        return Response({"reply":pk})

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        for data in serializer.data:
            print(data)
            user = User.objects.filter(id=data['user'])
            data['username'] = user[0].username
        return Response(serializer.data)

class UsersView(APIView):
     def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        print(request.user)
        return Response(usernames)

    