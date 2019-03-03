from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse
from login.models import Profile

from login.models import Profile

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class LoginPageView(TemplateView):
    template_name = 'pages/login_base.html'

class ProfilePageView(TemplateView):
    template_name = 'pages/profile_base.html'

def profile_page(request, computing_id):
    profile = Profile.objects.filter(computing_id = computing_id)
    user = {
        "users" : profile
    }
    return render(request, 'pages/profile.html', user)

    #return render(request, 'pages/profile.html', profile)

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
