from rest_framework import serializers
from .models import *


# class PostSerializer(serializers.ModelSerializer):
#     def create(self, validated_data):
#         post = Post.objects.create(posttText = validated_data['posText'] )
#         return post
#
#     class Meta:
#         model = Post
#         fields = '__all__' #('postText', 'pubDate', 'id')

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    firstname = serializers.CharField(source='user.first_name')

    class Meta:
        model = Profile
        fields = ('username', 'location', 'id'  , 'firstname' ,)


class PostSerializer(serializers.HyperlinkedModelSerializer):
    publisher = ProfileSerializer(read_only=True)
    detailedPost = serializers.CharField(write_only=True)

    class Meta:
        model = Post
        # comm = Post.get_comments(Post)
        fields = ('postText', 'id', 'publisher' , 'detailedPost')

    def create(self, validated_data):
        user = self.context['request'].user
        post = Post.objects.create(postText = validated_data.pop('postText') , publisher = Profile.objects.get(user=user))
        post.add_detailedPost(validated_data.pop('detailedPost'))
        return post



class detailedPostSerialzer(serializers.ModelSerializer):
    class Meta:
        model = DetailedPost
        fields = ('detailed',)


class PostSerializerAdd(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'  # ('postText', 'pubDate' , 'id', )


class ActivitySerializer(serializers.ModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = Activity
        fields = ('user', 'post')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    activity = ActivitySerializer()
    # post = serializers.CharField(source='activity.post')

    class Meta:
        model = Comment
        fields = ('comText', 'comDate', 'activity')

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     activity = validated_data.pop('activity')
    #     # post = validated_data.pop('activity.post')
    #     # print(post)
    #     #return post.add_comment(user=Profile.objects.get(user=user) , comText=validated_data.pop('comText'))

class AddCommentSerializer(serializers.ModelSerializer):
    post = serializers.CharField(write_only=True)
    class Meta:
        model = Comment
        fields = ('comText' , 'post')

    def create(self, validated_data):
        user = self.context['request'].user
        post = Post.objects.get(pk=validated_data.pop('post'))
        return post.add_comment(user=Profile.objects.get(user=user), comText=validated_data.pop('comText'))


class TagSerializer(serializers.ModelSerializer):
    # post = PostSerializer()

    class Meta:
        model = Tag
        fields = ( 'name', 'post')


class LikesSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = Like
        fields = ('url', 'likeDate', 'activity')



