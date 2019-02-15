from django.shortcuts import render

from .forms import NewProfileForm
from .models import Profile

from settings import LOGIN_REDIRECT_URL

def new_user(request):
    if request.method == 'POST':
        # check for form validity, save, redirect
        form = NewProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy(LOGIN_REDIRECT_URL))

    else request.method == 'POST':
        form = NewProfileForm()

    return render(request, 'login/new_user.html', {'form': form})
