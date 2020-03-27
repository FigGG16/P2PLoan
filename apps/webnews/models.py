from django.db import models
from DjangoUeditor.models import UEditorField
from users.models import UserProfile
from datetime import datetime
# Create your models here.



class News(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"公告标题")
    detail = UEditorField(verbose_name=u"公告详情",width=600, height=300, imagePath="news/ueditor/", filePath="news/ueditor/", default='')
    author = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name=u"作者", on_delete=models.CASCADE)
    publishTime = models.DateTimeField(verbose_name=u"发表时间时间")

    class Meta:
        verbose_name = u"公告"
        verbose_name_plural = verbose_name


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name