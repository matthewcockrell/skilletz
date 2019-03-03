from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse
from login.models import Profile, Comment

from login.models import Profile

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class LoginPageView(TemplateView):
    template_name = 'pages/login_base.html'

class ProfilePageView(TemplateView):
    template_name = 'pages/profile_base.html'

def profile_page(request, computing_id):
    comp = computing_id
    profile = Profile.objects.filter(computing_id = comp)
    comments = Comment.objects.filter(computing_id = comp)
    context = {
        "users" : profile,
        "comments" : comments
        }

    try:
        title = request.POST['title']
        description = request.POST['description']
        stars = request.POST['rating']
    except(KeyError):
        return render(request, 'pages/profile.html', context)

    else:
        comment = Comment(computing_id = comp, comment_title = title, comment_descr = description, rating = stars)
        comment.save()
        
    comments = Comment.objects.filter(computing_id = comp)
    context = {
        "users" : profile,
        "comments" : comments
        }
    return render(request, 'pages/profile.html', context)

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
