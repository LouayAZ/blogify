from rest_framework import serializers
from .models import *


# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ('postText', 'pubDate', 'id')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        # comm = Post.get_comments(Post)
        fields = ('postText', 'pubDate' , 'id', )



class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ('username', 'location', 'id')


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('user',)


class CommentSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = Comment
        fields = ('comText', 'comDate', 'activity')


class TagSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = Tag
        fields = ( 'name', 'post')


class LikesSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = Like
        fields = ('url', 'likeDate', 'activity')