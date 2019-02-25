from django.contrib.auth.models import User
from login.models import Profile
import django_filters

class ProfileFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = ['user', 'first_name', 'last_name', 'computing_id', 'major', 'graduation_year', ]