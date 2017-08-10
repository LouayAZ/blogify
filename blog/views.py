# Create your views here.

from django.http import HttpResponse

from .models import Post, Comment
from django.template import loader

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer


from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from blog.forms import UserForm , ProfileForm , SignInForm , UserLoginForm



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


def signin(request):
    if request.method == 'POST':
        signin_form = SignInForm(request.POST)
        if signin_form.is_valid():
            username = signin_form.cleaned_data['username']
            raw_password = signin_form.cleaned_data['password']
            user = authenticate(request, username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        signin_form = SignInForm()
    return render(request, 'blog/signin.html', {'form': signin_form})


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')

    return render(request,"blog/signin.html", {'form' : form})



class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts , many=True)
        return Response(serializer.data)

    def post(self):
        pass


def index(request):
    latest_post_list = Post.objects.order_by('-pubDate')[:5]
    template = loader.get_template('blog/index.html')
    context = {
        'latest_post_list': latest_post_list,
    }
    return HttpResponse(template.render(context, request))


def details(request, post_id):
    return HttpResponse("You're looking at post %s." % post_id)


def results(request, post_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % post_id)


def comment(request, post_id):
    return HttpResponse("You're commenting on question %s." % post_id)