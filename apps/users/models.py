

# Create your models here.
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.BidConst import BidConst
from django.contrib.auth.hashers import make_password,check_password
from utils.bitStatesUtils import BitStatesUtils

class UserProfile(AbstractUser):
    is_investor = models.BooleanField(default=False)
    is_borrower = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    trueName = models.CharField(max_length=50, verbose_name=u"真实昵称", default="")
    bornDate = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female")
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100, null=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"电话号码")
    kyc_complete = models.CharField(max_length=1, null=True, blank=True, verbose_name=u"验证程度")
    escrow_account_number = models.CharField(max_length=1, null=True, blank=True, verbose_name=u"银行存管账号")
    qq = models.CharField(max_length=10, null=True, blank=True, verbose_name=u"QQ号码")
    bitState = models.BigIntegerField(null=True,blank=True, default=0, verbose_name=u"用户状态码")
    real_auth_id = models.IntegerField(null=True, blank=True, verbose_name=u"实名认证表")
    identity_number = models.CharField(max_length=25, null=True, blank=True, verbose_name=u"身份证号码")
    score = models.IntegerField(blank=True,null=True, verbose_name="风控累计分数")

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

    def get_investor(self):
        return self.investor

    def isRealAuth(self):
        return BitStatesUtils.hasState(self.bitState,BitStatesUtils.GET_OP_REAL_AUTH())

    def isCheckInBasicInfo(self):
        return BitStatesUtils.hasState(self.bitState, BitStatesUtils.GET_OP_BASIC_INFO())

    def isVedioAuth(self):
        return BitStatesUtils.hasState(self.bitState, BitStatesUtils.GET_OP_VEDIO_AUTH())

    def isHasBidRequestProcess(self):
        return BitStatesUtils.hasState(self.bitState, BitStatesUtils.GET_OP_HAS_BIDREQUEST_PROCESS())

    def isBindBankInfo(self):
        return BitStatesUtils.hasState(self.bitState, BitStatesUtils.GET_OP_BIND_BANKINFO())

    def isMoneyWithoutProcess(self):
        return BitStatesUtils.hasState(self.bitState, BitStatesUtils.GET_HAS_MONEYWITHDRAW_PROCESS())

    def getScore(self):
        return self.score

    def addState(self, value):
        self.bitState = BitStatesUtils.addState(self.bitState, value)


    def removeState(self,value):
        self.bitState = BitStatesUtils.removeState(self.bitState, value)



    # __OP_BIND_PHONE = 1 << 0# 用户绑定手机状态码
    # __OP_BIND_EMAIL = 1 <<1# 用户绑定邮箱
    # __OP_BASIC_INFO = 1 <<2# 用户是否填写基本资料
    # __OP_REAL_AUTH = 1 <<3# 用户是否实名认证
    # __OP_VEDIO_AUTH = 1 <<4# 用户是否视频认证
    # __OP_HAS_BIDREQUEST_PROCESS = 1 <<5# 用户是否有一个借款正在处理流程当中
    # __OP_BIND_BANKINFO = 1 <<6# 用户是否绑定银行卡
    # __OP_HAS_MONEYWITHDRAW_PROCESS = 1 <<7 # 用户是否有一个提现申请在处理中


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


class Account(models.Model):

    userProfile = models.ForeignKey(UserProfile, verbose_name=u"用户名称", on_delete=models.CASCADE, null=True)
    usableAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),verbose_name="账户可用余额")
    freezedAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),verbose_name="账户冻结金额")
    unReceiveInterest = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),verbose_name="账户待收利息")
    unReceivePrincipal = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),verbose_name="账户待收本金")
    unReturnAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),verbose_name="账户待还金额")
    remainBorrowLimit = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),verbose_name="账户剩余授信额度")
    borrowLimit = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),verbose_name="账户授信额度")
    tradePassword = models.CharField(max_length=128,verbose_name="交易密码",null=True, blank=True)
    verifyCode = models.CharField(max_length=128,verbose_name="数据校验",null=True, blank=True)

    def getRemainBorrowLimit(self):
        return self.remainBorrowLimit


    def getTotalAmount(self):
        return self.usableAmount+self.freezedAmount+self.unReceivePrincipal

    def getUnReturnAmount(self):
        return self.unReturnAmount

    class Meta:
        verbose_name = "用户账户"
        verbose_name_plural = verbose_name

# 自定义密码加密
    def _set_password(self, password):
        self.password = make_password(password)

    def _check_password(self, password):
        return check_password(password, self.password)


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




