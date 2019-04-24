from django.shortcuts import render

from .forms import NewProfileForm
from .models import Profile

from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import logout
from django.views.generic import TemplateView

SHERRIFF_EMAIL = 'sherriff@gmail.com'
SHERRIFF_COMPUTING_ID = 'mss2x'

def new_user(request):
    if request.method == 'POST':
        form = NewProfileForm(request.POST)
        if form.is_valid():
            profile_to_save = form.save(commit=False) # don't commit yet so we can add the user
            
            form_email = request.user.email
            if '@virginia.edu' in form_email or form_email == SHERRIFF_EMAIL:
                #request.user.profile.profile_pic = profile_to_save.profile_pic
                request.user.profile.first_name = profile_to_save.first_name
                request.user.profile.last_name = profile_to_save.last_name
                request.user.profile.graduation_year = profile_to_save.graduation_year
                request.user.profile.major = profile_to_save.major
                #request.user.profile.resume = profile_to_save.resume

                if form_email == SHERRIFF_EMAIL:
                    request.user.profile.computing_id = SHERRIFF_COMPUTING_ID
                else:
                    at_symbol_index = form_email.find('@')
                    request.user.profile.computing_id = form_email[:at_symbol_index]

                request.user.profile.save()

                return redirect(reverse(settings.POST_LOGIN_HOME_URL))

    elif not request.user or ('@virginia.edu' not in request.user.email and request.user.email != SHERRIFF_EMAIL):
        request.user.delete()
        logout(request)
        return redirect(reverse('login:error'))
    elif request.user.profile and request.user.profile.has_been_initialized():
        return redirect(reverse(settings.POST_LOGIN_HOME_URL))

    else:
        form = NewProfileForm()

    return render(request, 'login/new_user.html', {'form': form})

class ErrorView(TemplateView):
    template_name = 'login/error.html'

def logout_user(request):
    logout(request)
    return redirect('pages:home')
