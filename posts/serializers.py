from rest_framework.serializers import (ModelSerializer)
from .models import *
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()

class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]
        extra_kwargs={"password":{"write_only":True}}
    
    def validate(self,data):
        username = data['username']
        users_names = User.objects.filter(username = username)
        if users_names.exists():
            raise ValidationError("This User is already Registerd")
        return data

    def create(self,validated_data):
        self.validate(validated_data)
        user_obj = User(
            username = validated_data['username'],
        )
        user_obj.set_password(validated_data['password'])
        user_obj.save()
        return validated_data

class PostSerializer(ModelSerializer):
    class Meta:
        model = PostModel
        fields = '__all__'

class LikeSerializer(ModelSerializer):
    class Meta:
        model = LikeModel
        fields = '__all__'

class ReplySerializer(ModelSerializer):
    class Meta:
        model = ReplyModel
        fields = '__all__'

class CommentSerializer(ModelSerializer):
    class Meta:
        model = CommentModel
        fields = '__all__'