# Generated by Django 2.2.6 on 2020-03-28 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0035_auto_20200328_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountflow',
            name='accountId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Account', verbose_name='用户账户'),
        ),
    ]