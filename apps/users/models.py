

# Create your models here.
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    is_investor = models.BooleanField(default=False)
    is_borrower = models.BooleanField(default=False)
    trueName = models.CharField(max_length=50, verbose_name=u"真实昵称", default="")
    bornDate = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female")
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100, null=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"电话号码")
    kyc_complete = models.CharField(max_length=1, null=True, blank=True, verbose_name=u"验证程度")
    escrow_account_number = models.CharField(max_length=1, null=True, blank=True, verbose_name=u"银行存管账号")
    qq = models.CharField(max_length=10, null=True, blank=True, verbose_name=u"QQ号码")
    bitState = models.BigIntegerField(null=True,blank=True,verbose_name=u"用户状态码")
    real_auth_id = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"实名认证表")

    def get_is_borrower(self):
        field_value = getattr(self, 'is_borrower')
        return field_value

    def is_type1(self):
        return self.is_borrower == True

    def is_type2(self):
        return self.is_investor == True

    class Meta:
        verbose_name = u"投资者"
        verbose_name_plural = verbose_name


    def get_borrower(self):
        return self.borrower


class BorrowerUserProfile(UserProfile):
    class Meta:
        verbose_name = "借款者"
        verbose_name_plural = verbose_name
        # 避免表重复
        proxy = True


class ManagerProfile(UserProfile):
    class Meta:
        verbose_name = "管理员"
        verbose_name_plural = verbose_name
        # 避免表重复
        proxy = True


class Investor(models.Model):
    userProfile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
    # id = models.AutoField(primary_key=True, default=1, verbose_name="用户ID")
    # 资料完善程度
    investment_limit = models.IntegerField(default=5000, verbose_name=u"投资限额")
    fund_committed = models.IntegerField(default=0, verbose_name=u"承诺金额")

    class Meta:
        verbose_name = '投资信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.userProfile.username


class Borrower(models.Model):
    HIGHEST_QUALIFICATION_CHOICE = (
        ('NONE', '无'),
        ('college', '大专'),
        ('bachelor', '本科'),
        ('master', '硕士'),
        ('doctor', '博士'),
    )

    MARRIAGE_STATE_CHOICE = (
        ('1', '未婚'),
        ('2', '已婚'),
        ('3', '丧偶'),
        ('4', '离婚'),
    )

    DWELLING_CONDITION_CHOICE = (
        ('1', '商品房'),
        ('2', '经济适用房'),
        ('3', '自建私有房'),
        ('4', '租赁房'),
        ('5', '单位福利分房'),
        ('6', '学生宿舍'),
    )
    userProfile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
    family_address = models.CharField(max_length=50, null=True, blank=True, verbose_name='家庭地址')
    highest_qualification = models.CharField(max_length=50, null=True, choices=HIGHEST_QUALIFICATION_CHOICE, blank=True,
                                             default='NONE', verbose_name=u"教育层次")
    pass_out_year = models.CharField(max_length=4, verbose_name=u"毕业日期", null=True, blank=True)
    university_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='大学名称')
    identity_number = models.CharField(max_length=25, null=True, blank=True, verbose_name=u"身份证号码")
    marriage_state = models.CharField(max_length=50, null=True, choices=MARRIAGE_STATE_CHOICE, blank=True,
                                              default='1', verbose_name=u"婚姻状况")
    dwelling_condition = models.CharField(max_length=50, null=True, choices=DWELLING_CONDITION_CHOICE, blank=True,
                                              default='1', verbose_name=u"住宅状况")
    dwelling_mobile = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"家庭电话号码")
    dwelling_time = models.CharField(max_length=5, null=True, blank=True, verbose_name=u"入住时间")
    is_buy_car = models.BooleanField(default=False, verbose_name=u"是否购车")

    def get_employment_detail(self):
        return self.employmentdetail_set.get(borrower_id=self.userProfile_id)

    class Meta:
        verbose_name = '借贷信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.userProfile.username


class EmploymentDetail(models.Model):
    EMPLOYMENT_STATE_CHOICE = (
        ('employment', '已就业'),
        ('unemployment', '待业'),
    )
    RECEIVING_WAGE_FROM = (
        ('bank', '银行'),
        ('cash', '现金'),
    )
    COMPANY_TYPE_CHOICE = (
        ('1', '国家行政企业'),
        ('2', '公私合作企业'),
        ('3', '中外合资企业'),
        ('4', '社会组织机构'),
        ('5', '国际组织机构'),
        ('6', '外资企业'),
        ('7', '私营企业'),
        ('8', '集体企业'),
        ('9', '国防军事企业'),
    )
    borrower = models.ForeignKey(Borrower, verbose_name=u"工作单位", on_delete=models.CASCADE)
    employment_state = models.CharField(max_length=30, null=True, choices=EMPLOYMENT_STATE_CHOICE, blank=True,
                                             default='无', verbose_name='就业状态')
    receive_wage = models.CharField(max_length=20, null=True, choices=RECEIVING_WAGE_FROM, blank=True,
                                             default='无', verbose_name='获得收入的方式')
    company_type = models.CharField(max_length=30, null=True, choices=COMPANY_TYPE_CHOICE, blank=True,
                                             default='无', verbose_name='公司类型')
    working_life = models.CharField(max_length=10, null=True, blank=True, verbose_name='工作年限')
    company_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='单位名称')
    working_department = models.CharField(max_length=30, null=True, blank=True, verbose_name='任职部门')
    company_address = models.CharField(max_length=200, null=True, blank=True, verbose_name='公司地址')
    company_mobile = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"公司电话号码")
    class Meta:
        verbose_name = u"工作详情"
        verbose_name_plural = verbose_name


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u"验证码类型", choices=(("register", u"注册"), ("forget", u"找回密码"), ("update_email", u"修改邮箱")), max_length=30)
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name


# 存储地
class Picture(models.Model):
    """This is a small demo using just two fields. The slug field is really not
    necessary, but makes the code simpler. ImageField depends on PIL or
    pillow (where Pillow is easily installable in a virtualenv. If you have
    problems installing pillow, use a more generic FileField instead.

    """
    file = models.ImageField(upload_to="pictures")
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.file.name

    # @models.permalink
    def get_absolute_url(self):
        return ('authentication_upload', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)

# class UserDataAuthentication(models.Model):
#     family_authentication_image
#     education_authentication_centent
#     phone_authentication
#     video_authentication
#     upload_message


class UsersFamilyAuthentication(models.Model):
    user_profile = models.ForeignKey(UserProfile, verbose_name=u"家庭验证", on_delete=models.CASCADE, null=True)
    is_authenticated = models.BooleanField(default=False)
    file = models.ImageField(upload_to="user_authentication_data/%Y", null=True, max_length=100)
    slug = models.SlugField(max_length=50, blank=True, null=True)

    # @models.permalink
    def get_absolute_url(self):
        return ('authentication_upload', )


    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(UsersFamilyAuthentication, self).save(*args, **kwargs)

    def save_user_profile_id(self, user):
        self.user_profile = user
        super(UsersFamilyAuthentication, self).save()

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(UsersFamilyAuthentication, self).delete(*args, **kwargs)


class UserVideoAuthentication(models.Model):
    user_profile = models.ForeignKey(UserProfile, verbose_name=u"视频验证", on_delete=models.CASCADE)
    is_authenticated = models.BooleanField(default=False)
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    slug = models.SlugField(max_length=50, blank=True, null=True)