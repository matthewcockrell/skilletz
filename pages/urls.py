from django.conf.urls import url
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'pages'

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url('login', views.LoginPageView.as_view(), name='login'),
    path(r'profile/<str:computing_id>', views.profile_page, name='profile_page'),
    url(r'profile$', login_required(views.ProfilePageView.as_view()), name='profile'),
    url(r'edit$', login_required(views.ProfileEditView.as_view()), name='edit_profile'),
    url('feed', login_required(views.search), name='feed'),
    url('availability', views.availability, name='availability'),
    path(r'like/<str:computing_id>', views.like_button, name='like'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
