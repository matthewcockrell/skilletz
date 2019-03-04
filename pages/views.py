from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .filters import ProfileFilter
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
        return reverse('pages:profile_page', kwargs={'computing_id':ProfileEditView.get_object(self).computing_id})

# Create your views here.
def search(request):
    profile_list = Profile.objects.all()
    profile_filter = ProfileFilter(request.GET, queryset=profile_list)
    return render(request, 'pages/profile_list.html', {'filter': profile_filter})

def availability(request):
    #if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        #form = NameForm(request.POST)
        # check whether it's valid:
        #if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
        #    return HttpResponseRedirect('/thanks/')
    # if a GET (or any other method) we'll create a blank form
    #else:
        #form = NameForm()

    days_to_view = []
    accessible_hours = []
    current_data = datetime.datetime.now()

    for i in range(7):
        month = current_data.month
        day = int(current_data.day)
        year = current_data.year
        list.append(days_to_view, "{}/{}/{}".format(
            month, day + i, year))

    for i in range(16):
        list.append(accessible_hours, "{}:00".format(9 + i))

    context = {
        "accessible_hours": accessible_hours,
        "days_to_view": days_to_view,
    }

    return render(request, 'pages/availability.html', context)


