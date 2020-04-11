from .views import *
from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns 
router = routers.DefaultRouter()

router.register('register',CreateUserViewset)
router.register('posts',PostsViewset)
router.register('likes',LikeViewset)
router.register('comments',CommentViewset)
router.register('replies',ReplyViewset)

urlpatterns = [
    path('get-users/', UsersView.as_view(), name='get_users'),
    path('logout/', Logout.as_view(), name='logout'),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
