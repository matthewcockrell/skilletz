from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

app_name = 'login'

urlpatterns = [
    url(r'new_user', views.new_user, name='new_user'),
    url(r'logout', views.logout_user, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
