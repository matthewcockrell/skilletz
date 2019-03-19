from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator

from .majors import UVA_MAJOR_CHOICES

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #profile_pic = models.ImageField(upload_to='images/')
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    graduation_year = models.PositiveSmallIntegerField(default=2000)
    major = models.CharField(max_length=100, choices=UVA_MAJOR_CHOICES, default='Undeclared')
    computing_id = models.CharField(max_length=7, default = '')
    #resume = models.FileField(upload_to='documents/')

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

class Course(models.Model):
    mnemonic = models.CharField(max_length=4, help_text='Ex. CS')
    number = models.PositiveSmallIntegerField(help_text='Ex. 3240', validators=[MaxValueValidator(9999)])
    title = models.CharField(max_length=100, help_text='Ex. Adv. Software Development Methods')

    def __str__(self):
        return '{} {}: {}'.format(self.mnemonic, self.number, self.title)

class Comment(models.Model):
    computing_id = models.CharField(max_length=7, default = '')
    comment_title = models.CharField(max_length = 500, default = '')
    comment_descr = models.TextField(null=True)
    rating = models.CharField(max_length = 10, default = 'one')

#class Hour(models.Model):
#    Date = models.CharField(max_length=10, default='')
 #   Hour = models.CharField(max_lenth=100,default='')

 #class Day(models.Model):
 #   Date = models.CharField(max_length=10, default='')
  #  Hour_9 = models.ManyToManyField(Hour, related_name= "Hour_9")
   # Hour_10 = models.ManyToManyField(Hour, related_name= "Hour_10")
    #Hour_11 = models.ManyToManyField(Hour, related_name= "Hour_11")
    #Hour_12 = models.ManyToManyField(Hour, related_name= "Hour_12")
    #Hour_13 = models.ManyToManyField(Hour, related_name= "Hour_13")
    #Hour_14 = models.ManyToManyField(Hour, related_name= "Hour_14")
    #Hour_15 = models.ManyToManyField(Hour, related_name= "Hour_15")
    #Hour_16 = models.ManyToManyField(Hour, related_name= "Hour_16")
    #Hour_17 = models.ManyToManyField(Hour, related_name= "Hour_17")
    #Hour_18 = models.ManyToManyField(Hour, related_name= "Hour_18")
    #Hour_19 = models.ManyToManyField(Hour, related_name= "Hour_19")
    #Hour_20 = models.ManyToManyField(Hour, related_name= "Hour_20")
    #Hour_21 = models.ManyToManyField(Hour, related_name= "Hour_21")
    #Hour_22 = models.ManyToManyField(Hour, related_name= "Hour_22")
    #Hour_23 = models.ManyToManyField(Hour, related_name= "Hour_23")
    #Hour_24 = models.ManyToManyField(Hour, related_name= "Hour_24")
