# Generated by Django 2.2.6 on 2020-03-22 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_userprofile_is_admin'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Banner',
        ),
        migrations.DeleteModel(
            name='Picture',
        ),
        migrations.RemoveField(
            model_name='uservideoauthentication',
            name='user_profile',
        ),
        migrations.DeleteModel(
            name='UsersFamilyAuthentication',
        ),
        migrations.DeleteModel(
            name='UserVideoAuthentication',
        ),
    ]
