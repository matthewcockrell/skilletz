from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse

from login.models import Profile

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class LoginPageView(TemplateView):
    template_name = 'pages/login_base.html'

class ProfilePageView(TemplateView):
    template_name = 'pages/profile.html'

class ProfileEditView(UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'graduation_year', 'major', 'computing_id']
    template_name_suffix = '_update_form'

    def get_object(self):
        return self.request.user.profile
    
    def get_success_url(self):
        return reverse('pages:profile')

class FeedPageView(TemplateView):
    template_name = 'pages/feed.html'

class AvailabilityPageView(TemplateView):
    template_name = 'pages/availability.html'
