from django.test import Client, TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from login.models import Profile, Course, Comment


#User navigates to the landing page
class TestViews(TestCase):

    def test_home_view(self):
        client = Client()
        response = client.get('/')
        self.assertTemplateUsed(response, "pages/home.html")

#User navigates to the "edit" page
    def test_edit(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = client.get("/edit")
        self.assertTemplateUsed(response, 'login/profile_update_form.html')

#User navigates to the "feed" page
    def test_feed(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = client.get('/feed')
        self.assertTemplateUsed(response, 'pages/profile_list.html')


#User leaves a comment and is re-directed back to that profile page
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

#Make sure comments are visible on the user's profile page
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

#Make sure the list of all profiles is visible on the feed
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

    def test_all_fields_visible_on_edit_page(self):
        client = Client()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = client.get('/edit')
        self.assertContains(response, "First name", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "Last name", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "Last name", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "Graduation year", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "Major", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "Computing id", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "Courses", count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response, "Bio", count=None, status_code=200, msg_prefix='', html=False)
    
