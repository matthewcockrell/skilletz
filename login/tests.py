from django.test import Client, TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse

from login import views

class TestLogin(TestCase):
    # Helper method
    def _login_and_create_profile(client):
        pass

    # T1: On login, user is redirected to google
    def test_google_oath_redirection(self):
        client = Client()
        response = client.get(reverse('pages:feed'))
        self.assertRedirects(response, '/oauth/login/google-oauth2/?next=/feed', fetch_redirect_response=False)

    # T7: A new user gets redirected to the profile creation page
    def test_redirection_to_profile_creation(self):
        fact = RequestFactory()
        req = fact.get(reverse('pages:feed'))
        req.user = User.objects.get_or_create(username='testuser1')[0]
        response = views.new_user(req)
        self.assertInHTML('Profile Creation', str(response.content))

    def test_redirection_to_feed_for_initialized_profile(self):
        fact = RequestFactory()
        req = fact.get(reverse('pages:feed'))
        req.user = User.objects.get_or_create(username='testuser1')[0]

        req.user.profile.first_name = 'Jimbo'
        req.user.profile.last_name = 'Jambo'
        req.user.profile.computing_id = 'abc3de'
        req.user.profile.save()

        response = views.new_user(req)
        self.assertRedirects(response, reverse('pages:feed'), fetch_redirect_response=False)

    def test_logout(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = client.logout()
        self.assertTemplateUsed(response, 'pages/home.html')
