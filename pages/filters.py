from django.contrib.auth.models import User
from login.models import Profile
import django_filters

class ProfileFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(label='First Name:', lookup_expr='icontains')
    last_name = django_filters.CharFilter(label = 'Last Name:', lookup_expr='icontains')
    computing_id = django_filters.CharFilter(label = 'Computing ID:', lookup_expr='icontains')
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'computing_id', 'major', 'availability', 'courses']
