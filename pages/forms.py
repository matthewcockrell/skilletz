from django.forms import ModelForm
from login.models import Profile

class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'first_name', 'last_name', 'graduation_year', 'major', 'computing_id', 'resume', 'courses', 'bio']
