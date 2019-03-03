from django.conf.urls import url
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'pages'

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url('login', views.LoginPageView.as_view(), name='login'),
    path(r'profile/<str:computing_id>', views.profile_page, name='profile'),
    url(r'profile$', login_required(views.ProfilePageView.as_view()), name='profile'),
    url(r'profile/edit$', login_required(views.ProfileEditView.as_view()), name='edit_profile'),
    url('feed', login_required(views.FeedPageView.as_view()), name='feed'),
    url('availability', login_required(views.AvailabilityPageView.as_view()), name='availability'),
]
