# Generated by Django 2.2.6 on 2020-02-28 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_auto_20200228_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidrequest',
            name='bidRequestState',
            field=models.IntegerField(blank=True, choices=[(0, '待发布'), (1, '招标中'), (2, '已撤销'), (3, '流标'), (4, '满标1审'), (5, '满标2审'), (6, '满标审核被拒绝'), (7, '还款中'), (8, '已还清'), (9, '逾期'), (10, '发标审核拒绝状态')], default=0, null=True, verbose_name='借款状态'),
        ),
    ]
