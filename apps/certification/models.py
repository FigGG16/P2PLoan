from django.db import models
from utils.bitStatesUtils import BitStatesUtils
from users.models import UserProfile
# Create your models here.


class BaseAudit(models.Model):


    CURRENT_STATE_CHOICE = (
        (BitStatesUtils.STATE_NORMAL(), '未审核'),
        (BitStatesUtils.STATE_AUDIT(), '审核通过'),
        (BitStatesUtils.STATE_REJECT(), '审核拒绝'),
    )
    remark = models.TextField(max_length=40, null=True, blank=True, verbose_name='审核备注')
    state = models.IntegerField(choices=CURRENT_STATE_CHOICE, default=0, blank=True, verbose_name='审核状态', null=True)
    applier = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name=u"申请人", on_delete=models.CASCADE)
    auditor = models.CharField(max_length=10, null=True, blank=True, verbose_name='审核人')
    applyTime = models.DateTimeField(auto_now_add=True, verbose_name=u"申请时间")
    audiTime = models.DateTimeField(blank=True, null=True, verbose_name=u"审核时间")

    class Meta:
        abstract = True


class RealAuth(BaseAudit):
    realName = models.CharField(max_length=10, null=True, blank=True, verbose_name='真实姓名')
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female")
    idNumber = models.CharField(max_length=25, null=True, blank=True, verbose_name=u"身份证号码")
    bornDate = models.DateField(verbose_name=u"生日", null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name='家庭地址')
    image1 = models.ImageField(upload_to="image/%Y/%m", max_length=100, null=True, blank=True, verbose_name='身份证正面地址')
    image2 = models.ImageField(upload_to="image/%Y/%m",  max_length=100, null=True, blank=True, verbose_name='身份证反面地址')
    file = models.ImageField(null=True)
    class Meta:
        verbose_name = u"待实名认证"
        verbose_name_plural = verbose_name


class RealAuthAuditted(RealAuth):
    class Meta:
        verbose_name = '已实名认证'
        verbose_name_plural = verbose_name
        # 这里必须设置proxy=True，这样就不会再生成一张表，同时还具有Model的功能
        proxy = True


#视频审核
class VedioAuth(BaseAudit):
    class Meta:
        verbose_name = u"视频认证"
        verbose_name_plural = verbose_name


class UserFile(BaseAudit):

    CHOICES = (
        (0, '无'),
        (1, '工作证明'),
        (2, '房产证正面'),
        (3, '房产证反面'),
        (4, '户口本'),
        (5, '结婚证'),
        (6, '银行流水证明'),
        (7, '学位证'),
        (8, '毕业证'),
    )
    image = models.ImageField(upload_to="image/%Y/%m", max_length=100, null=True, blank=True, verbose_name='分控材料图片')
    fileType = models.IntegerField(default=0, null=True, choices=CHOICES, blank=True, verbose_name='分控材料分类')
    score = models.IntegerField(null=True, blank=True, verbose_name='分控材料评分')
    class Meta:
        verbose_name = u"风控材料认证"
        verbose_name_plural = verbose_name


class UserFileAudit(UserFile):
    class Meta:
        verbose_name = '风控材料已认证'
        verbose_name_plural = verbose_name
        # 这里必须设置proxy=True，这样就不会再生成一张表，同时还具有Model的功能
        proxy = True


