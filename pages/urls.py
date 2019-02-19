from django.conf.urls import url

from . import views

app_name = 'pages'

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url('login', views.LoginPageView.as_view(), name='login'),
    url('profile', views.ProfilePageView.as_view(), name='profile'),
    url('feed', views.FeedPageView.as_view(), name='feed')
]
