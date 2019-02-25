from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'pages'

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url('login', views.LoginPageView.as_view(), name='login'),
    url('profile', login_required(views.ProfilePageView.as_view()), name='profile'),
    url('feed', login_required(views.search), name='feed'),
]
