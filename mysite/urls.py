"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url , include
from django.contrib import admin
from blog import views , urls
from rest_framework import routers
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
# routers.register(r'Post', views.PostViewSet)
router.register(r'Profile', views.ProfileViewSet , 'profile')
router.register(r'Post' , views.PostViewSet , 'post')
router.register(r'Comment' , views.PostCommentsViewSet , 'comment')
router.register(r'Followers' , views.FollowerViewSet , 'followers')
router.register(r'Like' , views.PostLikesViewSet , 'like')
router.register(r'Tags' , views.PostTagsViewSet , 'tag')
router.register(r'TagPosts', views.TagPostsViewSet , 'TagPosts')
router.register(r'FriendsPosts', views.FriendsPostsViewSet , 'friendsPosts')
router.register(r'SharedPosts', views.SharedPostsViewSet , 'SharedPosts')
router.register(r'PostAdd' , views.PostAddViewSet , 'postadd')
router.register(r'DetailedPost' , views.detailedPostViewSet , 'detailedPost')

router1 = routers.DefaultRouter(trailing_slash=False)
router1.registry = router.registry[:]

urlpatterns =[
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^', include(router1.urls)),
    url(r'^blog/', include('blog.urls')),
   ]

