from django.forms import ModelForm
from login.models import Profile

class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = [ 'first_name', 'last_name', 'graduation_year', 'major', 'computing_id', 'availability', 'courses', 'bio']
