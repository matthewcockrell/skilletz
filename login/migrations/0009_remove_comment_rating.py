# Generated by Django 2.1.5 on 2019-03-03 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_auto_20190303_0407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='rating',
        ),
    ]
