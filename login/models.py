from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .majors import UVA_MAJOR_CHOICES

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    graduation_year = models.PositiveSmallIntegerField(default=2000)
    major = models.CharField(max_length=100, choices=UVA_MAJOR_CHOICES, default='Undeclared')
    computing_id = models.CharField(max_length=7, default = '')

    def has_been_initialized(self):
        return len(self.first_name) > 0 or len(self.last_name) > 0 or self.graduation_year != 2000 or self.major != 'Undeclared' or self.computing_id != ''

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Comment(models.Model):
    computing_id = models.CharField(max_length=7, default = '')
    comment_title = models.CharField(max_length = 500, default = '')
    comment_descr = models.TextField(null=True)
    rating = models.CharField(max_length = 10, default = 'one')
