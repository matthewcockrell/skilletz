from django.test import Client, TestCase
from django.contrib.auth.models import User

#T6: User navigates to the landing page
class TestViews(TestCase):
    def test_home_view(self):
        client = Client()
        response = client.get('/')
        self.assertTemplateUsed(response, "pages/home.html")

#T9: User navigates to the "edit" page
    def test_edit(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = client.get("/edit")
        self.assertTemplateUsed(response, 'login/profile_update_form.html')

#T17: User navigates to the "feed" page
    def test_feed(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = client.get('/feed')
        self.assertTemplateUsed(response, 'pages/profile_list.html')

#T13: User leaves a comment and is re-directed back to that profile page
    def test_comment_reload(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = client.get('/profile/mdc3kw') #Test on this by using my profile
        response = client.post('/profile/mdc3kw')
        self.assertTemplateUsed(response, 'pages/profile.html')
