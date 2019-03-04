from django.test import TestCase
from django.test import Client, TestCase
from django.contrib.auth.models import User
from login.models import Profile

# Create your tests here.
class TestViews(TestCase):
    def test_feed_populate(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        profile_list = Profile.objects.all()
        request = client.get('/feed/',{'first_name':'Marina', 'last_name':'Kun'})
        self.assertEqual(len(filter.qs),1)