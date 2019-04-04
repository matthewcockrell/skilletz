from django.shortcuts import render

from .forms import NewProfileForm, EditProfileForm
from .models import Profile

from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import logout

def new_user(request):
    if request.method == 'POST':
        form = NewProfileForm(request.POST)
        if form.is_valid():
            profile_to_save = form.save(commit=False) # don't commit yet so we can add the user

            request.user.profile.first_name = profile_to_save.first_name
            request.user.profile.last_name = profile_to_save.last_name
            request.user.profile.graduation_year = profile_to_save.graduation_year
            request.user.profile.major = profile_to_save.major
            request.user.profile.computing_id = profile_to_save.computing_id

            request.user.profile.save()

            return redirect(reverse(settings.POST_LOGIN_HOME_URL))

    elif request.user.profile and request.user.profile.has_been_initialized():
        return redirect(reverse(settings.POST_LOGIN_HOME_URL))

    else:
        form = NewProfileForm()

    return render(request, 'login/new_user.html', {'form': form})



def edit_user(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile_to_save = form.save(commit=False)

            #request.user.profile.profile_pic = profile_to_save.profile_pic
            request.user.profile.first_name = profile_to_save.first_name
            request.user.profile.last_name = profile_to_save.last_name
            request.user.profile.graduation_year = profile_to_save.graduation_year
            request.user.profile.major = profile_to_save.major
            request.user.profile.computing_id = profile_to_save.computing_id
            #request.user.profile.resume = profile_to_save.resume

            request.user.profile.save()

            return redirect(reverse('pages/profile.html'))

    return render(request, 'login/profile_update_form.html', {'form' : form})


def logout_user(request):
    logout(request)
    return redirect('pages:home')
