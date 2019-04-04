from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator

from .majors import UVA_MAJOR_CHOICES
class Hour(models.Model):
    class Meta:
        ordering = ('day', 'hour')

    day = models.PositiveSmallIntegerField(help_text='Index of day within week (Ex. Sun = 0, Mon = 1, ... Sat = 6)')
    hour = models.PositiveSmallIntegerField(help_text='Index of hor within day (Ex. 12am = 0, 1am = 1, ... 11pm = 23)')
    display_text = models.CharField(max_length=20, help_text='display string used in views')

    def __str__(self):
        return self.display_text
class Course(models.Model):
    class Meta:
        ordering = ('mnemonic', 'number',)

    mnemonic = models.CharField(max_length=4, help_text='Ex. CS')
    number = models.PositiveSmallIntegerField(help_text='Ex. 3240', validators=[MaxValueValidator(9999)])
    title = models.CharField(max_length=100, help_text='Ex. Adv. Software Development Methods')

    def __str__(self):
        return '{} {}: {}'.format(self.mnemonic, self.number, self.title)

class Identifier(models.Model):
    computing_id = models.TextField(null=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #profile_pic = models.ImageField(upload_to='images/', default='', blank=True)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    graduation_year = models.PositiveSmallIntegerField(default=2000)
    major = models.CharField(max_length=100, choices=UVA_MAJOR_CHOICES, default='Undeclared')
    computing_id = models.CharField(max_length=7, default = '')
    #resume = models.FileField(upload_to='documents/', default='', blank=True)
    courses = models.ManyToManyField(Course)
    bio = models.TextField(null=True)
    availability = models.ManyToManyField(Hour, through='AvailabilityEntry')
    people_who_I_like = models.ManyToManyField(Identifier, related_name = 'people_who_I_like')
    people_who_like_me = models.ManyToManyField(Identifier, related_name = 'people_who_like_me')

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

class AvailabilityEntry(models.Model):
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    notes = models.CharField(max_length=50, help_text='Additional notes for this hour')


class Comment(models.Model):
    computing_id = models.CharField(max_length=7, default = '')
    comment_title = models.CharField(max_length = 500, default = '')
    comment_descr = models.TextField(null=True)
    rating = models.CharField(max_length = 10, default = 'one')
