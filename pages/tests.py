from django.test import Client, TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from login.models import Profile, Course, Comment, Hour, Identifier
from django.test import LiveServerTestCase
#from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from pages import views

'''References:
Django Testing Tools Documentation:    https://docs.djangoproject.com/en/2.1/topics/testing/tools
'''

class TestViews(TestCase):

#T7: User navigates to the landing page
    def test_home_view(self):
        client = Client()
        response = client.get('/')
        self.assertTemplateUsed(response, "pages/home.html")

#T10: User navigates to the "edit" page
    def test_edit(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = client.get("/edit")
        self.assertTemplateUsed(response, 'login/profile_update_form.html')



#T11: User navigates to the "edit" page, updates their information, and those updates are reflected on their profile
    def test_update_on_edit_page(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        fact = RequestFactory()
        req = fact.get(reverse('pages:edit_profile'))
        req.user = User.objects.get_or_create(username='testuser1')[0]
        req.user.profile.first_name = 'Student'
        req.user.profile.last_name = 'Student'
        req.user.profile.computing_id = 'abc123'
        req.user.profile.bio = 'third-year CS major'
        req.user.profile.save()
        response = views.ProfileEditView.as_view()
        response = client.get('/profile/abc123')
        self.assertContains(response, "third-year CS major", count=None, status_code=200, msg_prefix='', html=False)
        req = fact.get(reverse('pages:edit_profile'))
        req.user = User.objects.get_or_create(username='testuser1')[0]
        req.user.profile.first_name = 'Student'
        req.user.profile.last_name = 'Student'
        req.user.profile.computing_id = 'abc123'
        req.user.profile.bio = 'second-year CS major'
        req.user.profile.save()
        response = views.ProfileEditView.as_view()
        response = client.get('/profile/abc123')
        self.assertContains(response, "second-year CS major", count=None, status_code=200, msg_prefix='', html=False)


#User navigates to the "feed" page
    def test_feed(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = client.get('/feed')
        self.assertTemplateUsed(response, 'pages/profile_list.html')


#T14: User leaves a comment and is re-directed back to that profile page
    def test_comment_reload(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = client.post('/profile/mdc3kw')
        self.assertTemplateUsed(response, 'pages/profile.html')

#Make sure the user's bio is visible on the profile page
    def test_bio_visible_on_profile(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        req = client.get(reverse('pages:feed'))
        req.user = User.objects.get_or_create(username='testuser1')[0]
        req.user.profile.first_name = 'Student'
        req.user.profile.last_name = 'Student'
        req.user.profile.computing_id = 'abc123'
        req.user.profile.bio = 'third-year CS major'
        req.user.profile.save()
        response = client.get('/profile/abc123')
        self.assertContains(response, "third-year CS major", count=None, status_code=200, msg_prefix='', html=False)

#Make sure the user's current courses are visible on the profile page
    def test_courses_visible_on_profile(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        req = client.get(reverse('pages:feed'))
        req.user = User.objects.get_or_create(username='testuser1')[0]
        req.user.profile.first_name = 'Student'
        req.user.profile.last_name = 'Student'
        req.user.profile.computing_id = 'abc123'
        course = Course.objects.create(mnemonic='CS', number=3240, title='Advanced Software Development')
        req.user.profile.courses.add(course)
        req.user.profile.save()
        response = client.get('/profile/abc123')
        self.assertContains(response, "Advanced Software Development", count=None, status_code=200, msg_prefix='', html=False)

#T15: Make sure comments are visible on the user's profile page
    def test_comments_visible_on_profile(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        req = client.get(reverse('pages:feed'))
        req.user = User.objects.get_or_create(username='testuser1')[0]
        req.user.profile.first_name = 'Student'
        req.user.profile.last_name = 'Student'
        req.user.profile.computing_id = 'abc123'
        req.user.profile.bio = 'third-year CS major'
        req.user.profile.save()
        comment = Comment.objects.create(computing_id='abc123', comment_title='Great!', comment_descr='helpful and easy to work with', rating='five')
        comment.save()
        response = client.get('/profile/abc123')
        self.assertContains(response, "helpful and easy to work with", count=None, status_code=200, msg_prefix='', html=False)

#T18: Make sure the list of all profiles is visible on the feed
    def test_profile_list_visible_on_feed(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        req1 = client.get(reverse('pages:feed'))
        req2 = client.get(reverse('pages:feed'))
        req1.user1 = User.objects.get_or_create(username = 'alice')[0]
        req1.user1.profile.first_name = 'Alice'
        req1.user1.profile.last_name = 'Smith'
        req1.user1.profile.major = "Computer Science"
        req1.user1.profile.computing_id = 'abc123'
        req1.user1.profile.save()
        req2.user2 = User.objects.get_or_create(username = 'bob')[0]
        req2.user2.profile.first_name = 'Bob'
        req2.user2.profile.last_name = 'Jones'
        req2.user2.profile.major = "English"
        req2.user2.profile.computing_id = 'xyz987'
        req2.user2.profile.save()
        response = client.get('/feed')
        self.assertContains(response, "Alice", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "Bob", count=None, status_code=200, msg_prefix='', html=False)

#Make sure that when information is updated in the database, it is reflected visibly on the user's profile
    def test_update_information(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        req = client.get(reverse('pages:feed'))
        req.user = User.objects.get_or_create(username='testuser1')[0]
        req.user.profile.first_name = 'Student'
        req.user.profile.last_name = 'Student'
        req.user.profile.computing_id = 'abc123'
        req.user.profile.bio = 'third-year CS major'
        req.user.profile.save()
        response = client.get('/profile/abc123')
        self.assertContains(response, "Student", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "third-year CS major", count=None, status_code=200, msg_prefix='', html=False)
        req.user.profile.computing_id = 'xyz987'
        req.user.profile.bio = 'second-year CS major'
        req.user.profile.save()
        response = client.get('/profile/xyz987')
        self.assertContains(response, "Student", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "second-year CS major", count=None, status_code=200, msg_prefix='', html=False)

#Make sure that all of the required fields are visible on the edit page
    def test_all_fields_visible_on_edit_page(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = client.get('/edit')
        self.assertContains(response, "First name", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "Last name", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "Last name", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "Graduation year", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "Major", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "Courses", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "Bio", count=None, status_code=200, msg_prefix='', html=False)

#T23: Make sure that the navbar is visible on top of all pages, EXXCEPT the landing page
    def test_navbar_visible_on_all_pages(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        req = client.get(reverse('pages:feed'))
        req.user = User.objects.get_or_create(username='testuser1')[0]
        req.user.profile.computing_id = 'abc123'
        req.user.profile.save()
        response = client.get('/feed')
        self.assertContains(response, "Main Feed", count=None, status_code=200, msg_prefix='', html=False)
        response = client.get('/profile/abc123')
        self.assertContains(response, "Main Feed", count=None, status_code=200, msg_prefix='', html=False)
        response = client.get('/edit')
        self.assertContains(response, "Main Feed", count=None, status_code=200, msg_prefix='', html=False)
        response = client.get('/')
        self.assertNotContains(response, "Main Feed", status_code=200, msg_prefix='', html=False)

#T26: Make sure that updates to a user's availability appear on their profile page
    def test_update_availability(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        req1 = client.get(reverse('pages:feed'))
        req1.user1 = User.objects.get_or_create(username = 'alice')[0]
        req1.user1.profile.first_name = 'Alice'
        req1.user1.profile.last_name = 'Smith'
        req1.user1.profile.major = "Computer Science"
        req1.user1.profile.computing_id = 'abc123'
        hour = Hour.objects.create(day = 0, hour = 12, display_text = 'Sunday 12 PM')
        req1.user1.profile.availability.add(hour)
        req1.user1.profile.save()
        response = client.get('/profile/abc123')
        self.assertContains(response, "Sunday 12 PM", status_code=200, msg_prefix='', html=False)

#T27: User "likes" another user, and that is reflected on the "people_I_like" list on their personal profile
    def test_you_like_another_person(self):
        client = Client()
        req1 = client.get(reverse('pages:feed'))
        req2 = client.get(reverse('pages:feed'))
        req1.user1 = User.objects.get_or_create(username = 'alice')[0]
        req1.user1.profile.first_name = 'Alice'
        req1.user1.profile.last_name = 'Smith'
        req1.user1.profile.major = "Computer Science"
        req1.user1.profile.computing_id = 'abc123'
        req2.user2 = User.objects.get_or_create(username = 'bob')[0]
        req2.user2.profile.first_name = 'Bob'
        req2.user2.profile.last_name = 'Jones'
        req2.user2.profile.major = "English"
        req2.user2.profile.computing_id = 'xyz987'
        liker = Identifier.objects.create(liker = 'xyz987', liked = 'abc123') #Bob "likes" Alice
        liked = Identifier.objects.create(liked = 'abc123', liker = 'xyz987') #Bob "likes" Alice
        req2.user2.profile.people_who_I_like.add(liked)
        req1.user1.profile.people_who_like_me.add(liker)
        req1.user1.profile.save()
        req2.user2.profile.save()
        client.force_login(req2.user2)
        response = client.get("/profile/xyz987")
        self.assertContains(response, "abc123", status_code=200, msg_prefix='', html=False)

#T28: Another user "likes" you, and that is reflected on the "people_who_like_me" list on their personal profile
    def test_another_person_likes_you(self):
        client = Client()
        req1 = client.get(reverse('pages:feed'))
        req2 = client.get(reverse('pages:feed'))
        req1.user1 = User.objects.get_or_create(username = 'alice')[0]
        req1.user1.profile.first_name = 'Alice'
        req1.user1.profile.last_name = 'Smith'
        req1.user1.profile.major = "Computer Science"
        req1.user1.profile.computing_id = 'abc123'
        req1.user1.profile.save()
        req2.user2 = User.objects.get_or_create(username = 'bob')[0]
        req2.user2.profile.first_name = 'Bob'
        req2.user2.profile.last_name = 'Jones'
        req2.user2.profile.major = "English"
        req2.user2.profile.computing_id = 'xyz987'
        liker = Identifier.objects.create(liker = 'xyz987', liked = 'abc123') #Bob "likes" Alice
        liked = Identifier.objects.create(liked = 'abc123', liker = 'xyz987') #Bob "likes" Alice
        req2.user2.profile.people_who_I_like.add(liked)
        req1.user1.profile.people_who_like_me.add(liker)
        req1.user1.profile.save()
        req2.user2.profile.save()
        client.force_login(req1.user1)
        response = client.get("/profile/abc123")
        self.assertContains(response, "xyz987", status_code=200, msg_prefix='', html=False)

#T29: The matching lists should only appear on the profile of the user who is logged in
#`    They should not be able to see any other user's lists
    def test_matching_visibility(self):
        client = Client()
        req1 = client.get(reverse('pages:feed'))
        req2 = client.get(reverse('pages:feed'))
        req1.user1 = User.objects.get_or_create(username = 'alice')[0]
        req1.user1.profile.first_name = 'Alice'
        req1.user1.profile.last_name = 'Smith'
        req1.user1.profile.major = "Computer Science"
        req1.user1.profile.computing_id = 'abc123'
        req1.user1.profile.save()
        req2.user2 = User.objects.get_or_create(username = 'bob')[0]
        req2.user2.profile.first_name = 'Bob'
        req2.user2.profile.last_name = 'Jones'
        req2.user2.profile.major = "English"
        req2.user2.profile.computing_id = 'xyz987'
        liker = Identifier.objects.create(liker = 'xyz987', liked = 'abc123') #Bob "likes" Alice
        liked = Identifier.objects.create(liked = 'abc123', liker = 'xyz987') #Bob "likes" Alice
        req2.user2.profile.people_who_I_like.add(liked)
        req1.user1.profile.people_who_like_me.add(liker)
        req1.user1.profile.save()
        req2.user2.profile.save()
        client.force_login(req1.user1) #Log in as Alice
        response = client.get("/profile/abc123") #Go to her profile
        self.assertContains(response, "People Who I Like", status_code=200, msg_prefix='', html=False) #list should be visible on her profile
        self.assertContains(response, "People Who Like Me", status_code=200, msg_prefix='', html=False) #List should be visible on her profile
        client.logout()
        client.force_login(req2.user2) #Log in as Bob
        response = client.get("/profile/abc123") #Go to Alice's profile while logged in as Bob
        self.assertNotContains(response, "People Who I Like", status_code=200, msg_prefix='', html=False) #List should NOT be visible
        self.assertNotContains(response, "People Who Like Me", status_code=200, msg_prefix='', html=False) #List should NOT be visible

    #You unlike another user, so it should no longer appear in your "people_I_like" list on your profile
    def test_you_unlike_another_person(self):
        client = Client()
        req1 = client.get(reverse('pages:feed'))
        req2 = client.get(reverse('pages:feed'))
        req1.user1 = User.objects.get_or_create(username = 'alice')[0]
        req1.user1.profile.first_name = 'Alice'
        req1.user1.profile.last_name = 'Smith'
        req1.user1.profile.major = "Computer Science"
        req1.user1.profile.computing_id = 'abc123'
        req1.user1.profile.save()
        req2.user2 = User.objects.get_or_create(username = 'bob')[0]
        req2.user2.profile.first_name = 'Bob'
        req2.user2.profile.last_name = 'Jones'
        req2.user2.profile.major = "English"
        req2.user2.profile.computing_id = 'xyz987'
        liker = Identifier.objects.create(liker = 'xyz987', liked = 'abc123') #Bob "likes" Alice
        liked = Identifier.objects.create(liked = 'abc123', liker = 'xyz987') #Bob "likes" Alice
        req2.user2.profile.people_who_I_like.add(liked)
        req1.user1.profile.people_who_like_me.add(liker)
        req1.user1.profile.save()
        req2.user2.profile.save()
        client.force_login(req1.user1)
        response = client.get("/profile/xyz987") #Go to Bob's profile
        self.assertContains(response, "abc123", status_code=200, msg_prefix='', html=False) #Does alice show up there?
        req2.user2.profile.people_who_I_like.remove(liked)
        req1.user1.profile.people_who_like_me.remove(liker)
        liker.delete()
        liked.delete()
        response = client.get("/profile/xyz987") #Go to Bob's profile again
        self.assertContains(response, "abc123", status_code=200, msg_prefix='', html=False) #Does alice show up there?


    #Another user unlikes you, so it should no longerappear in your "people_who_like_me" list in your profile
    def test_another_user_unlikes_you(self):
        client = Client()
        req1 = client.get(reverse('pages:feed'))
        req2 = client.get(reverse('pages:feed'))
        req1.user1 = User.objects.get_or_create(username = 'alice')[0]
        req1.user1.profile.first_name = 'Alice'
        req1.user1.profile.last_name = 'Smith'
        req1.user1.profile.major = "Computer Science"
        req1.user1.profile.computing_id = 'abc123'
        req1.user1.profile.save()
        req2.user2 = User.objects.get_or_create(username = 'bob')[0]
        req2.user2.profile.first_name = 'Bob'
        req2.user2.profile.last_name = 'Jones'
        req2.user2.profile.major = "English"
        req2.user2.profile.computing_id = 'xyz987'
        liker = Identifier.objects.create(liker = 'xyz987', liked = 'abc123') #Bob "likes" Alice
        liked = Identifier.objects.create(liked = 'abc123', liker = 'xyz987') #Bob "likes" Alice
        req2.user2.profile.people_who_I_like.add(liked)
        req1.user1.profile.people_who_like_me.add(liker)
        req1.user1.profile.save()
        req2.user2.profile.save()
        client.force_login(req1.user1)
        response = client.get("/profile/abc123") #Go to alice's profile
        self.assertContains(response, "xyz987", status_code=200, msg_prefix='', html=False) #Does Bob show up there?
        req2.user2.profile.people_who_I_like.remove(liked)
        req1.user1.profile.people_who_like_me.remove(liker)
        liker.delete()
        liked.delete()
        response = client.get("/profile/abc123") #Go to alice's profile again
        self.assertNotContains(response, "xyz987", status_code=200, msg_prefix='', html=False) #Does bob Show up there?

    def test_like_button_change_to_unlike(self):
        client = Client()
        req1 = client.get(reverse('pages:feed'))
        req2 = client.get(reverse('pages:feed'))
        req1.user1 = User.objects.get_or_create(username = 'alice')[0]
        req1.user1.profile.first_name = 'Alice'
        req1.user1.profile.last_name = 'Smith'
        req1.user1.profile.major = "Computer Science"
        req1.user1.profile.computing_id = 'abc123'
        req1.user1.profile.save()
        req2.user2 = User.objects.get_or_create(username = 'bob')[0]
        req2.user2.profile.first_name = 'Bob'
        req2.user2.profile.last_name = 'Jones'
        req2.user2.profile.major = "English"
        req2.user2.profile.computing_id = 'xyz987'
        liker = Identifier.objects.create(liker = 'xyz987', liked = 'abc123')
        liked = Identifier.objects.create(liked = 'abc123', liker = 'xyz987')
        req2.user2.profile.people_who_I_like.add(liked)
        req1.user1.profile.people_who_like_me.add(liker)
        req1.user1.profile.save()
        req2.user2.profile.save()
        client.force_login(req2.user2)
        response = client.get("/profile/abc123")
        self.assertContains(response, "Unlike", status_code=200, msg_prefix='', html=False) #Unlike button should appear
        self.assertNotContains(response, "Like!", status_code=200, msg_prefix='', html=False) #Like button should not be there

    def test_unlike_button_change_back_to_like(self):
        client = Client()
        req1 = client.get(reverse('pages:feed'))
        req2 = client.get(reverse('pages:feed'))
        req1.user1 = User.objects.get_or_create(username = 'alice')[0]
        req1.user1.profile.first_name = 'Alice'
        req1.user1.profile.last_name = 'Smith'
        req1.user1.profile.major = "Computer Science"
        req1.user1.profile.computing_id = 'abc123'
        req1.user1.profile.save()
        req2.user2 = User.objects.get_or_create(username = 'bob')[0]
        req2.user2.profile.first_name = 'Bob'
        req2.user2.profile.last_name = 'Jones'
        req2.user2.profile.major = "English"
        req2.user2.profile.computing_id = 'xyz987'
        liker = Identifier.objects.create(liker = 'xyz987', liked = 'abc123')
        liked = Identifier.objects.create(liked = 'abc123', liker = 'xyz987')
        req2.user2.profile.people_who_I_like.add(liked)
        req1.user1.profile.people_who_like_me.add(liker)
        req1.user1.profile.save()
        req2.user2.profile.save()
        client.force_login(req2.user2)
        response = client.get("/profile/abc123")
        self.assertContains(response, "Unlike", status_code=200, msg_prefix='', html=False) #Unlike button should appear
        self.assertNotContains(response, "Like!", status_code=200, msg_prefix='', html=False) #Like button should not be there
        req2.user2.profile.people_who_I_like.remove(liked)
        req1.user1.profile.people_who_like_me.remove(liker)
        liker.delete()
        liked.delete()
        response = client.get("/profile/abc123")
        self.assertContains(response, "Like!", status_code=200, msg_prefix='', html=False) #Unlike button should not be there
        self.assertNotContains(response, "Unlike", status_code=200, msg_prefix='', html=False) #Like button should re-appear
