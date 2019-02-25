from django.shortcuts import render
from django.views.generic import TemplateView
from .filters import ProfileFilter
from login.models import Profile

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class LoginPageView(TemplateView):
    template_name = 'pages/login_base.html'

class ProfilePageView(TemplateView):
    template_name = 'pages/profile.html'

# Create your views here.
def search(request):
    profile_list = Profile.objects.all()
    profile_filter = ProfileFilter(request.GET, queryset=profile_list)
    return render(request, 'pages/profile_list.html', {'filter': profile_filter})