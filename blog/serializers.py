from rest_framework import serializers
from .models import Post , Relationship , Profile


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class FollowerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ('username', 'location' , 'id')