# Generated by Django 2.2.6 on 2020-03-10 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('certification', '0016_auto_20200220_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBanknInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bankName', models.CharField(blank=True, max_length=50, null=True, verbose_name='银行名称')),
                ('accountName', models.CharField(blank=True, max_length=50, null=True, verbose_name='开户人姓名')),
                ('accountNumber', models.CharField(blank=True, max_length=50, null=True, verbose_name='银行账号')),
                ('bankForkName', models.CharField(blank=True, max_length=50, null=True, verbose_name='开户支行')),
                ('userProfile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userBanknInfos', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户银行卡',
                'verbose_name_plural': '用户银行卡',
            },
        ),
    ]
