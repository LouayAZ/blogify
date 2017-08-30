# Create your views here.
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template import loader
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from blog.forms import *
from .serializers import *


def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            # user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()

            profile_form = ProfileForm(request.POST,
                                       instance=user.profile)  # Reload the profile form with the profile instance
            profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            profile_form.save()

            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'blog/signup.html', {'form': user_form , 'profile_form':profile_form})


class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class FollowerViewSet(viewsets.ModelViewSet):
    # person = Profile.objects.get(pk = 15)
    person = get_object_or_404(Profile, pk=11)
    queryset = person.get_following()
    serializer_class = ProfileSerializer

    def retrieve(self, request, pk = 11):
        user = get_object_or_404(Profile, pk=pk)
        queryset = user.get_following()
        if not queryset:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer_class = ProfileSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class PostCommentsViewSet(viewsets.ModelViewSet):
    id = 8
    print(id)
    post = Post.objects.get(pk = id)
    queryset = post.get_comments()
    serializer_class = CommentSerializer

    def retrieve(self, request, pk=None):
        post= Post.objects.get(pk = pk)
        queryset = post.get_comments()
        if not queryset:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer_class = CommentSerializer(queryset , many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)


class PostTagsViewSet(viewsets.ModelViewSet):
    id = 10
    post = Post.objects.get(pk=id)
    # post = Tag.post.through.objects.get(pk = id)
    queryset = post.get_tags()
    serializer_class = TagSerializer

    def retrieve(self, request, pk=None):
        post = Post.objects.get(pk = pk)
        queryset = post.get_tags()
        if not queryset:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer_class = TagSerializer(queryset , many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)


class TagPostsViewSet(viewsets.ModelViewSet):
    id = 1
    tag = Tag.objects.get(pk=id)
    # post = Tag.post.through.objects.get(pk = id)
    queryset = tag.get_posts()
    serializer_class = PostSerializer

    def retrieve(self, request, pk=None):
        tag = Tag.objects.get(pk = pk)
        queryset = tag.get_posts()
        if not queryset:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer_class = PostSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)


class PostLikesViewSet(viewsets.ModelViewSet):
    id =10
    post = Post.objects.get(pk = id)
    queryset = post.get_likes()
    serializer_class = LikesSerializer

    def retrieve(self, request, pk=None):
        post = Post.objects.get(pk=id)
        queryset = post.get_likes()
        if not queryset:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer_class = LikesSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)


class FriendsPostsViewSet(viewsets.ModelViewSet):
    id = 11
    user = get_object_or_404(Profile, pk=id)
    friends = user.get_following()

    queryset = Post.objects.filter(publisher__in =friends)
    serializer_class = PostSerializer

    def retrieve(self, request, pk=None):
        user = get_object_or_404(Profile, pk=pk)
        friends = user.get_following()

        queryset = Post.objects.filter(publisher__in =friends)

        if not queryset:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer_class = PostSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)


# class SharedPosts(viewsets.ModelViewSet):
#     id = 11
#     user = get_object_or_404(Profile, pk=id)
#     queryset = user.get_shared_posts()
#     serializer_class = PostSerializer
#
#     def retrieve(self, request, pk=None):
#         user = get_object_or_404(Profile, pk=pk)
#         queryset = user.get_shared_posts()
#
#         if not queryset:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         else:
#             serializer_class = PostSerializer(queryset, many=True)
#             return Response(serializer_class.data, status=status.HTTP_200_OK)


def index(request):
    latest_post_list = Post.objects.order_by('-pubDate')[:5]
    template = loader.get_template('blog/index.html')
    context = {
        'latest_post_list': latest_post_list,
    }
    return HttpResponse(template.render(context, request))


def details(request, post_id):
    post = Post.objects.get(pk=post_id)
    return HttpResponse("%s." % post)


def results(request, post_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % post_id)


def comment(request, post_id):
    if request.method == 'POST':
            commentform = CommentForm(request.POST)
            post = Post.objects.get(pk=post_id)

            if request.user.is_authenticated:
                print(request.user.id)
                user = Profile.objects.get(user=request.user)
                post.add_comment(user, commentform.data.get('comment'))
            else:
                print("la3")
            return redirect('index')
    else:
        commentform = CommentForm()
    return render(request, 'blog/pforms.html', {'title' : "add comment" , 'form': commentform })

    # return HttpResponse("You're commenting on question %s." % post_id)


def post(request):
    if request.method == 'POST':
        postform = PostForm(request.POST)

        if request.user.is_authenticated:
            user = Profile.objects.get(user=request.user)
            user.add_post(postform.data.get('postTitle') , postform.data.get('detailedPost'))
        return redirect('index')
    else:
        postform = PostForm()
    return render(request , 'blog/pforms.html' , {'title' : "add post" , 'form': postform })


def like(request , post_id):
    if request.method == 'POST':
            post = Post.objects.get(pk=post_id)

            if request.user.is_authenticated:
                print(request.user.id)
                user = Profile.objects.get(user=request.user)
                post.like(user)
            else:
                print("la3")
            return redirect('index')
    return render(request , 'blog/pforms.html' , {'title' : "like"})

def bookmark(request , post_id):
    if request.method == 'POST':
            post = Post.objects.get(pk=post_id)

            if request.user.is_authenticated:
                print(request.user.id)
                user = Profile.objects.get(user=request.user)
                post.bookmark(user)
            else:
                print("la3")
            return redirect('index')
    return render(request , 'blog/pforms.html' , {'title' : "bookmark"})


def share(request , post_id):
    if request.method == 'POST':
            post = Post.objects.get(pk=post_id)

            if request.user.is_authenticated:
                print(request.user.id)
                user = Profile.objects.get(user=request.user)
                post.share(user)
            else:
                print("la3")
            return redirect('index')
    return render(request , 'blog/pforms.html' , {'title' : "like"})