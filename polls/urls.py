from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

#create url namespace to avoid conflicts across apps
app_name = 'polls'

urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^mypoll', login_required(views.MyPollView.as_view()), name='mypoll'),
	url(r'^create', views.create, name='create'),
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
	url(r'^(?P<pk>[0-9]+)/results/$', views.ResultView.as_view(), name='results'),
	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),	
]