# Generated by Django 2.1.5 on 2019-03-03 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_comment_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.CharField(default='one', max_length=10),
        ),
    ]
