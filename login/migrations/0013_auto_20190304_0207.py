# Generated by Django 2.1.7 on 2019-03-04 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0012_auto_20190304_0054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='day',
            name='Hour_10',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_11',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_12',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_13',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_14',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_15',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_16',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_17',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_18',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_19',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_20',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_21',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_22',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_23',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_24',
        ),
        migrations.RemoveField(
            model_name='day',
            name='Hour_9',
        ),
        migrations.DeleteModel(
            name='Day',
        ),
        migrations.DeleteModel(
            name='Hour',
        ),
    ]
