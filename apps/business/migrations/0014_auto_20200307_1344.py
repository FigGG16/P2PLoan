# Generated by Django 2.2.6 on 2020-03-07 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0013_auto_20200305_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='ublishBidAaudit',
            fields=[
            ],
            options={
                'verbose_name': '发标前审核',
                'verbose_name_plural': '发标前审核',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('business.bidrequestaudithistory',),
        ),
        migrations.AlterField(
            model_name='accountflow',
            name='accountId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Account', verbose_name='用户账户'),
        ),
    ]
