from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class PostModel(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    content = models.TextField()
    no_of_likes = models.IntegerField(default=0)
    no_of_comments = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post_id)

class CommentModel(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel,on_delete=models.CASCADE) # Many to One RelationShip
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment_id)

class ReplyModel(models.Model):
    reply_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel,on_delete=models.CASCADE) # Many to One RelationShip
    comment = models.ForeignKey(CommentModel,on_delete=models.CASCADE) # Many to One RelationShip
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

class LikeModel(models.Model):
    like_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel,on_delete=models.CASCADE) # Many to One RelationShip

    

    def __str__(self):
        return str(self.user)


