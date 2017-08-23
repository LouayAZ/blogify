from rest_framework import serializers
from .models import Post , Relationship , Profile , Comment , Activity


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class FollowerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ('username', 'location', 'id')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('url', 'postText', 'pubDate', 'publisher' , 'id')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ('username', 'location', 'id')

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('user' ,)

class CommentSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = Comment
        fields = ('comText' , 'comDate' , 'activity' )