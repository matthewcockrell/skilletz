# Generated by Django 2.1.7 on 2019-04-04 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0021_auto_20190404_0443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availabilityentry',
            name='hour',
        ),
        migrations.RemoveField(
            model_name='availabilityentry',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='availability',
        ),
        migrations.AddField(
            model_name='profile',
            name='times',
            field=models.ManyToManyField(to='login.Hour'),
        ),
        migrations.DeleteModel(
            name='AvailabilityEntry',
        ),
    ]