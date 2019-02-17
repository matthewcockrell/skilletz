from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url('login', views.LoginPageView.as_view(), name='login')
]
