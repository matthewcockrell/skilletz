from django.forms import ModelForm

from .models import Profile

class NewProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'first_name', 'last_name', 'graduation_year', 'major', 'computing_id', 'resume']
