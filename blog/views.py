# Create your views here.

from django.http import HttpResponse

from .models import Post , Comment
from django.template import loader

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer

class PostList(APIView):

    def get(self , request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts , many=True )
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