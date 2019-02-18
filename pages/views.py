from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class LoginPageView(TemplateView):
    template_name = 'pages/login_base.html'

class ProfilePageView(TemplateView):
    template_name = 'pages/profile.html'

class FeedPageView(TemplateView):
    template_name = 'pages/feed.html'