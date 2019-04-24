from django.forms import ModelForm
from login.models import Profile
from django import forms

class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'graduation_year', 'major', 'courses', 'availability', 'bio']
