# Generated by Django 2.1.7 on 2019-04-04 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0022_auto_20190404_1838'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='times',
            new_name='availability',
        ),
    ]
