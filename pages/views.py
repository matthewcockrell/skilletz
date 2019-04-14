import datetime
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import ModelFormMixin
from .filters import ProfileFilter
from .forms import ProfileEditForm
from django.views.generic.edit import UpdateView
from django.urls import reverse
from login.models import Profile, Comment, Course, Identifier

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
    identify = Identifier(liked = computing_id, liker = request.user.profile.computing_id)
    bool = True
    people = request.user.profile.people_who_I_like.all()
    for person in people:
        if person.liked == computing_id:
            bool = False

    context = {
        "users" : profile,
        "comments" : comments,
        "bool" : bool
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
        "comments" : comments,
        "bool" : bool
        }
    return render(request, 'pages/profile.html', context)

def like_button(request, computing_id):
    comp = computing_id
    profile = Profile.objects.filter(computing_id = comp)
    identify_who_I_like = Identifier(liked = computing_id, liker=request.user.profile.computing_id)
    identify_who_likes_me = Identifier(liked = computing_id, liker=request.user.profile.computing_id)
    identify_who_I_like.save()
    identify_who_likes_me.save()
    list = request.user.profile.people_who_I_like.all()
    list2 = []
    for person in list:
        list2.append(person.liked) #list of everyone that I like
    if identify_who_I_like.liked in list2:
        to_del = Identifier.objects.all()
        request.user.profile.people_who_I_like.remove(identify_who_I_like)
        profile[0].people_who_like_me.remove(identify_who_likes_me)
        for d in to_del:
            if d.liked == computing_id and d.liker == request.user.profile.computing_id:
                d.delete()
        identify_who_I_like.delete()
        identify_who_likes_me.delete()
        redir = '/profile/' + computing_id
    else:
        request.user.profile.people_who_I_like.add(identify_who_I_like)
        profile[0].people_who_like_me.add(identify_who_likes_me)
        redir = '/profile/' + computing_id
    return redirect(redir)

class ProfileEditView(UpdateView):
    model = Profile
    form_class = ProfileEditForm
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

    list.append(days_to_view, "Sunday")
    list.append(days_to_view, "Monday")
    list.append(days_to_view, "Tuesday")
    list.append(days_to_view, "Wednesday")
    list.append(days_to_view, "Thursday")
    list.append(days_to_view, "Friday")
    list.append(days_to_view, "Saturday")


    list.append(accessible_hours, "9:00")
    for i in range(15):
        list.append(accessible_hours, "{}:00".format(10 + i))

    context = {
        "accessible_hours": accessible_hours,
        "days_to_view": days_to_view,
    }

    return render(request, 'pages/availability.html', context)
