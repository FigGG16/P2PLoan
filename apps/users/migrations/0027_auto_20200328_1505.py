# Generated by Django 2.2.6 on 2020-03-28 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_auto_20200322_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='qq',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='QQ号码'),
        ),
    ]
