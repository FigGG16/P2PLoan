# Generated by Django 2.2.6 on 2020-02-28 14:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidrequest',
            name='applyTime',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='这个标的申请时间'),
        ),
        migrations.AlterField(
            model_name='bidrequest',
            name='bidRequestType',
            field=models.IntegerField(blank=True, choices=[(0, '普通信用标'), (1, '普通信用标')], null=True, verbose_name='借款类型(信用标)'),
        ),
        migrations.AlterField(
            model_name='bidrequest',
            name='returnType',
            field=models.IntegerField(blank=True, choices=[(0, '按月分期还款'), (1, '按月到期还款')], null=True, verbose_name='还款类型(等额本息)'),
        ),
        migrations.CreateModel(
            name='BidRequestAuditHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.TextField(blank=True, max_length=40, null=True, verbose_name='审核备注')),
                ('state', models.IntegerField(blank=True, choices=[(0, '未审核'), (1, '审核通过'), (2, '审核拒绝')], default=0, null=True, verbose_name='审核状态')),
                ('auditor', models.CharField(blank=True, max_length=10, null=True, verbose_name='审核人')),
                ('applyTime', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('audiTime', models.DateTimeField(blank=True, null=True, verbose_name='审核时间')),
                ('auditType', models.IntegerField(blank=True, choices=[(0, '未审核'), (1, '审核通过'), (2, '审核拒绝')], default=0, null=True, verbose_name='审核状态')),
                ('applier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='申请人')),
                ('bidRequestId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.BidRequest', verbose_name='标')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
