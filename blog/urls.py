from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /post/5/
    url(r'^(?P<post_id>[0-9]+)/$', views.details, name='detail'),
    # ex: /post/5/results/
    url(r'^(?P<post_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /post/5/vote/
    url(r'^(?P<post_id>[0-9]+)/comment/$', views.comment, name='comment'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login, {'template_name': 'blog/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]