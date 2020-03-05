# Generated by Django 2.2.6 on 2020-03-01 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_auto_20200228_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformBankInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bankName', models.CharField(blank=True, max_length=50, null=True, verbose_name='银行名称')),
                ('accountName', models.CharField(blank=True, max_length=50, null=True, verbose_name='开户人姓名')),
                ('accountNumber', models.CharField(blank=True, max_length=50, null=True, verbose_name='银行账号')),
                ('bankForkName', models.CharField(blank=True, max_length=50, null=True, verbose_name='开户支行')),
            ],
            options={
                'verbose_name': '平台账户',
                'verbose_name_plural': '平台账户',
            },
        ),
    ]