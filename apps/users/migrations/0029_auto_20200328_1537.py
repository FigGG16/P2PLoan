# Generated by Django 2.2.6 on 2020-03-28 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_auto_20200328_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='score',
            field=models.IntegerField(blank=True, default=0, verbose_name='风控累计分数'),
        ),
    ]