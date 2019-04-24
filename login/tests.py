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

    #T2: On login, a current user is re-directed to the feed page upon logging in
    def test_redirection_to_feed_for_initialized_profile(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser', email='abc3de@virginia.edu')[0])

        fact = RequestFactory()
        req = fact.get(reverse('pages:feed'))
        req.user = User.objects.get_or_create(username='testuser1', email='abc3de@virginia.edu')[0]

        req.user.profile.first_name = 'Jimbo'
        req.user.profile.last_name = 'Jambo'
        req.user.profile.save()

        response = views.new_user(req)
        self.assertRedirects(response, reverse('pages:feed'), fetch_redirect_response=False)

    #T3: User logs in and sees the "login" button be replaced with the "logout" button in the nav-bar
    def test_login_change_to_logout(self):
            client = Client()
            response = client.get('/')
            self.assertContains(response, "Login", count=None, status_code=200, msg_prefix='', html=False)
            client.force_login(User.objects.get_or_create(username='testuser', email='abc3de@virginia.edu')[0])
            response = client.get('/feed')
            self.assertContains(response, "Logout", count=None, status_code=200, msg_prefix='', html=False)

    #T4: Currently logged in user navigates to different page and sees the logout button remain in place in the nav-bar
    def test_logout_remains_in_place(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser', email='abc3de@virginia.edu')[0])
        response = client.get('/feed')
        self.assertContains(response, "Logout", count=None, status_code=200, msg_prefix='', html=False)
        response = client.get('/edit')
        self.assertContains(response, "Logout", count=None, status_code=200, msg_prefix='', html=False)


    #T5: User logs out of the system and re-directed to the main landing page
    def test_logout(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser', email='abc3de@virginia.edu')[0])
        response = client.logout()
        self.assertTemplateUsed(response, 'pages/home.html')


    #T6: User logs out of the system and sees the "logout" button replace by the "login" button in the nav-bar
    def test_logout_change_to_login(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser', email='abc3de@virginia.edu')[0])
        response = client.get('/feed')
        self.assertContains(response, "Logout", count=None, status_code=200, msg_prefix='', html=False)
        response = client.logout()
        response = client.get('/')
        self.assertContains(response, "Login", count=None, status_code=200, msg_prefix='', html=False)

    # T8: A new user gets redirected to the profile creation page
    def test_redirection_to_profile_creation(self):
        fact = RequestFactory()
        req = fact.get(reverse('pages:feed'))
        req.user = User.objects.get_or_create(username='testuser1', email='abc3de@virginia.edu')[0]
        response = views.new_user(req)
        self.assertInHTML('Profile Creation', str(response.content))

    #T9: A new user enters their information into the "create profile" form, and this is reflected on their new profile
    def test_create_new_user(self):
        client = Client()
        user = User.objects.get_or_create(username='testuser1', email='abc3de@virginia.edu')[0]
        client.force_login(user)

        fact = RequestFactory()
        req = fact.get(reverse('pages:feed'))
        req.user = user

        response = views.new_user(req)
        self.assertInHTML('Profile Creation', str(response.content))

        req.user.profile.first_name = 'Jimbo'
        req.user.profile.last_name = 'Jambo'
        req.user.profile.computing_id= 'abc3de'
        req.user.profile.save()

        client.force_login(User.objects.get_or_create(username='testuser2', email='uv9xyz@virginia.edu')[0])
        response = client.get('/profile/abc3de')

        self.assertContains(response, "Jimbo", count=None, status_code=200, msg_prefix='', html=False)
