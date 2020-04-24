from django.db import models
from decimal import *
# Create your models here.
from utils.BidConst import BidConst
from users.models import Borrower, Investor, Account,UserProfile
from certification.models import BaseAudit
from utils.DecimalFormatUtil import DecimalFormatUtil

class BidRequest(models.Model):

    RETURN_TYPE_CHOICE =(
        (0, "按月分期还款"),
        (1, "按月到期还款")
    )
    BID_REQUEST_TYPE_CHOICE = (
        (0, "普通信用标"),
        (1, "普通信用标")
    )

    BID_REQUEST_STATE = (
        (0,"待发布"),
        (1,"招标中"),
        (2,"已撤销"),
        (3,"流标"),
        (4,"满标1审"),
        (5,"满标2审"),
        (6,"满标审核被拒绝"),
        (7,"还款中"),
        (8,"已还清"),
        (9,"逾期"),
        (10,"发标审核拒绝状态"),
         )

    returnType = models.IntegerField(null=True, blank=True, choices=RETURN_TYPE_CHOICE, verbose_name="还款类型(等额本息)")
    bidRequestType = models.IntegerField(null=True, blank=True, choices=BID_REQUEST_TYPE_CHOICE, verbose_name="借款类型(信用标)")
    bidRequestState = models.IntegerField(null=True,choices=BID_REQUEST_STATE, default=BidConst.GET_BIDREQUEST_STATE_PUBLISH_PENDING(),blank=True, verbose_name="借款状态")
    bidRequestAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="借款总金额")
    currentRate = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="年化利率")#//
    minBidAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="最小借款金额") #// 最小借款金额
    monthes2Return = models.IntegerField(null=True, blank=True, verbose_name="还款月数")#// 还款月数
    bidCount = models.IntegerField(null=True, blank=True, verbose_name="已投标次数(冗余)",default=0) #//
    totalRewardAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="总回报金额(总利息)")#// 总回报金额(总利息)
    currentSum = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="当前已投标总金额") #// 当前已投标总金额
    title = models.CharField(max_length=50,blank=True, null=True, verbose_name="借款标题")#// 借款标题
    description = models.TextField(max_length=100, null=True, blank=True, verbose_name="借款描述")#// 借款描述
    note = models.TextField(max_length=100, null=True, blank=True, verbose_name="风控意见")#// 风控意见
    disableDate = models.DateTimeField(blank=True,null=True, verbose_name=u"招标截止日期") #// 招标截止日期
    disableDays = models.IntegerField(null=True, blank=True, verbose_name="招标天数") #// 招标天数
    createUser = models.ForeignKey(Borrower, verbose_name=u"借款人", on_delete=models.CASCADE)#// 借款人
    #
    # bids #// 针对该借款的投标
    #
    applyTime = models.DateTimeField(auto_now_add=True,null=True, verbose_name=u"这个标的申请时间")#// 申请时间
    #
    publishTime = models.DateTimeField(blank=True,null=True, verbose_name=u"发标时间")# #// 发标时间

    # / **
    # *计算当前投标进度
    # * /
    # return currentSum.divide(bidRequestAmount, BidConst.DISPLAY_SCALE,
    #                          RoundingMode.HALF_UP).multiply(new
    # BigDecimal("100"));
    # }
    # / **
    # *计算还需金额
    #
    # getRemainAmount()
    # {
    # return DecimalFormatUtil.formatBigDecimal(
    #     bidRequestAmount.subtract(currentSum), BidConst.DISPLAY_SCALE);
    # }
    #
    # / **
    # *计算当前投标进度
    # * /
    def getPersent(self):
        return (self.currentSum / self.bidRequestAmount) * Decimal('100')

    # / **
    # *计算还需金额
    #
    def getRemainAmount(self):
        return DecimalFormatUtil.formatBigDecimal(self.bidRequestAmount - self.currentSum, BidConst.DISPLAY_SCALE())

    def isFullBid(self):
        return self.currentSum == self.bidRequestAmount

    def get_bided_count(self):
        return self.bids.count()

    class Meta:
        verbose_name = u"借款对象表"
        verbose_name_plural = verbose_name

class Bid(models.Model):

    actualRate = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(), verbose_name="年化利率")#// (等同于bidrequest上的currentRate)
    availableAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(), verbose_name="这次投标金额")# // 这次投标金额
    bidRequestId = models.ForeignKey(BidRequest,related_name='bids', verbose_name=u"借款标来源", on_delete=models.CASCADE)#// 关联借款 来自于哪个借款标
    bidRequestTitle = models.CharField(max_length=50,blank=True, null=True, verbose_name="借款标题")#// 冗余数据, 等同于借款标题
    bidUser = models.ForeignKey(Investor, verbose_name=u"投标人", on_delete=models.CASCADE)#// 借款人#// 投标人
    bidTime = models.DateTimeField(blank=True,null=True, verbose_name=u"投标时间")#// 投标时间
    class Meta:
        verbose_name = u"一次投资对象表"
        verbose_name_plural = verbose_name
    # bidRequestState #// 不保存到数据库中, 只供查询使用


class BidRequestAuditHistory(BaseAudit):
    AUDIT_TYPE_STATE_CHOICE = (
        (0, '发标前审核'),
        (1, '满标一审'),
        (2, '满标二审'),
    )
    PUBLISH_AUDIT = 0 #// 发标前审核
    FULL_AUDIT_1 = 1 #// 满标一审
    FULL_AUDIT_2 = 2 #// 满标二审
    bidRequestId = models.ForeignKey(BidRequest, verbose_name=u"标对象", on_delete=models.CASCADE)
    auditType = models.IntegerField(choices=AUDIT_TYPE_STATE_CHOICE, default=PUBLISH_AUDIT, blank=True, verbose_name='审核状态', null=True)

    class Meta:
        verbose_name = u"所有标的审核历史"
        verbose_name_plural = verbose_name

    def getAuditTypeDisplay(self):
        return self.auditType


class PublishBidAaudit(BidRequestAuditHistory):

    class Meta:
        verbose_name = '发标前审核'
        verbose_name_plural = verbose_name
        # 这里必须设置proxy=True，这样就不会再生成一张表，同时还具有Model的功能
        proxy = True

class FullAuditOne(BidRequestAuditHistory):

    class Meta:
        verbose_name = '满标一审'
        verbose_name_plural = verbose_name
        # 这里必须设置proxy=True，这样就不会再生成一张表，同时还具有Model的功能
        proxy = True


class FullAuditTwo(BidRequestAuditHistory):
    class Meta:
        verbose_name = '满标二审'
        verbose_name_plural = verbose_name
        # 这里必须设置proxy=True，这样就不会再生成一张表，同时还具有Model的功能
        proxy = True



class PlatformBankInfo(models.Model):

    BANK_NAME_CCHOICE = (
        (1 , "中国工商银行"),
        (2 , "中国农业银行"),
        (3 , "中国建设银行"),
        (4 , "中国招商银行"),
        (5 , "中国民生银行"),
        (6 , "中国交通银行"),
        (7 , "中国银行"),
        (8 , "中信银行"),
        (9 , "广发银行"),
        (10, "兴业银行"),
        (11, "华夏银行"),
        (12, "上海银行"),
        (13, "北京银行"),
        (14, "光大银行"),
        (15, "平安银行"),
        (16, "中国信合"),
        (17, "广州银行"),
        (18, "南京银行"),
        (19, "深圳发展银行"),
        (20, "中国邮政储蓄银行"),
        (21, "浦发银行"),
        (22, "广州农村商业银行"),)

    bankName = models.IntegerField(blank=True, choices=BANK_NAME_CCHOICE, null=True, verbose_name="银行名称")# // 银行名称
    accountName = models.CharField(max_length=50,blank=True, null=True, verbose_name="开户人姓名") #// 开户人姓名
    accountNumber = models.CharField(max_length=50,blank=True, null=True, verbose_name="银行账号") #// 银行账号
    bankForkName = models.CharField(max_length=50,blank=True, null=True, verbose_name="开户支行") # // 开户支行

    class Meta:
        verbose_name = u"平台账户"
        verbose_name_plural = verbose_name


class RechargeOffline(BaseAudit):

    bankInfo = models.ForeignKey(PlatformBankInfo, verbose_name=u"平台账户", on_delete=models.CASCADE)
    tradeCode = models.CharField(max_length=50,blank=True, null=True, verbose_name="交易号") #// 交易号
    amount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="充值金额") #// 充值金额
    tradeTime = models.DateTimeField(blank=True,null=True, verbose_name=u"充值时间")#// 充值时间
    note = models.TextField(max_length=40, null=True, blank=True, verbose_name='充值说明')# // 充值说明

    class Meta:
        verbose_name = u"充值审核"
        verbose_name_plural = verbose_name

class AccountFlow(models.Model):

    ACCOUNT_TYPE = (
        (0,"线下充值"),
        (1,"提现成功"),
        (2,"成功借款"),
        (3,"成功投标"),
        (4,"还款"),
        (5,"回款"),
        (6,"支付平台管理费"),
        (7,"利息管理费"),
        (8,"提现手续费"),
        (9,"充值手续费"),
        (10,"投标冻结金额"),
        (11, "取消投标冻结金额"),
        (12, "提现申请冻结金额"),
        (13, "提现申请失败取消冻结金额"),
         )

    accountId = models.ForeignKey(Account, verbose_name=u"用户账户", on_delete=models.CASCADE) #// 流水是关于哪个账户的
    amount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                       verbose_name="变化的余额") #// 这次账户发生变化的金额
    tradeTime = models.DateTimeField(blank=True,null=True, verbose_name=u"变化的时间") #// 这次账户发生变化的时间
    accountType = models.IntegerField(blank=True,null=True,choices=ACCOUNT_TYPE,verbose_name="资金变化类型") #// 资金变化类型
    usableAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                       verbose_name="变化之后的可用余额")#// 发生变化之后的可用余额;
    freezedAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                       verbose_name="变化之后的冻结金额") #// 发生变化之后的冻结金额;
    note = models.TextField(max_length=100, null=True, blank=True, verbose_name="账户流水说明") #; // 账户流水说明

    class Meta:
        verbose_name = u"账户流水"
        verbose_name_plural = verbose_name


class SystemAccount(models.Model):
    usableAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                       verbose_name="平台账户剩余金额")
    freezedAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="平台账户冻结金额")
    class Meta:
        verbose_name = u"平台账户"
        verbose_name_plural = verbose_name

class SystemAccountFlow(models.Model):


    ACCOUNT_ACTION_TYPE_CCHOICE = (
        (1 , "账户管理费"),
        (2 , "利息管理费"),
        (3 , "提现手续费"),
    )
    amount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                 verbose_name="变化的余额")  # // 这次账户发生变化的金额
    accountActionType = models.IntegerField(blank=True, null=True, choices=ACCOUNT_ACTION_TYPE_CCHOICE, verbose_name="资金变化类型")  # // 资金变化类型
    createdTime = models.DateTimeField(auto_now_add=True,blank=True, null=True, verbose_name=u"创建时间")  # // 这次账户发生变化的时间
    usableAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                       verbose_name="平台账户剩余金额")
    freezedAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="平台账户冻结金额")
    note = models.TextField(max_length=100, null=True, blank=True, verbose_name="系统账户流水说明") #; // 账户流水说明
    systemAccountId = models.ForeignKey(SystemAccount, verbose_name=u"用户账户", on_delete=models.CASCADE)  # // 流水是关于哪个账户的

    class Meta:
        verbose_name = u"平台账户流水"
        verbose_name_plural = verbose_name


class PaymentSchedule(models.Model):
    RETURN_TYPE_CHOICE =(
        (0, "按月分期还款"),
        (1, "按月到期还款")
    )
    STATE_CHOICE= (
        (0, "正常待还"),
        (1, "已还"),
        (2, "逾期")
    )
    BID_REQUEST_TYPE_CHOICE = (
        (0, "普通信用标"),
        (1, "普通信用标")
    )
    bidRequestId = models.ForeignKey(BidRequest,related_name='PaymentSchedules',null=True, verbose_name=u"借款标", on_delete=models.CASCADE)#; // 对应借款
    bidRequestTitle = models.CharField(max_length=50,blank=True, null=True, verbose_name="借款名称")# // 借款名称
    borrower = models.ForeignKey(Borrower, verbose_name=u"还款人",null=True,related_name='PaymentSchedules', on_delete=models.CASCADE)#; // 还款人
    deadLine = models.DateTimeField(null=True, verbose_name=u"本期还款截止期限") # // 本期还款截止期限
    payDate = models.DateTimeField(null=True, verbose_name=u"还款时间") # // 还款时间
    totalAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="本期还款总金额")#// // 本期还款总金额，利息 + 本金
    principal = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="本期还款本金")#// 本期还款本金
    interest = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="本期还款总利息")# // 本期还款总利息
    monthIndex = models.IntegerField(null=True, blank=True, verbose_name="第几期")#// 第几期(即第几个月)
    state = BidConst.PAYMENT_STATE_NORMAL = models.IntegerField(null=True, blank=True,default=BidConst.GET_PAYMENT_STATE_NORMAL(),choices=STATE_CHOICE,verbose_name="本期还款状态")# // 本期还款状态（默认正常待还）
    bidRequestType = models.IntegerField(null=True, blank=True, choices=BID_REQUEST_TYPE_CHOICE, verbose_name="借款类型(信用标)") #// 借款类型
    returnType = models.IntegerField(null=True, blank=True, choices=RETURN_TYPE_CHOICE, verbose_name="还款方式")#// 还款方式，等同借款(BidRequest)

    class Meta:
        verbose_name = u"还款计划"
        verbose_name_plural = verbose_name

class PaymentScheduleDetail(models.Model):
    RETURN_TYPE_CHOICE =(
        (0, "按月分期还款"),
        (1, "按月到期还款")
    )
    bidAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="总共投标金额")# // 该投标人总共投标金额, 便于还款 / 垫付查询
    bidId = models.ForeignKey(Bid,null=True,related_name='PaymentScheduleDetails', verbose_name=u"借款标来源", on_delete=models.CASCADE)#// 关联借款 来自于哪个借款标
    totalAmount =  models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="本期还款总金额")# // 本期还款总金额( = 本金 + 利息)
    principal = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="本期应还款本金")# // 本期应还款本金
    interest = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="本期应还款利息")#// 本期应还款利息
    monthIndex = models.IntegerField(null=True, blank=True, verbose_name="第几期")#// 第几期(即第几个月)
    deadline = models.DateTimeField(null=True, verbose_name=u"本期还款截止期限") #// 本期还款截止时间
    bidRequestId = models.ForeignKey(BidRequest, null=True,related_name='PaymentScheduleDetails', verbose_name=u"借款标", on_delete=models.CASCADE) #// 所属哪个借款
    payDate = models.DateTimeField(null=True, verbose_name=u"实际付款日期") #  // 实际付款日期
    returnType = models.IntegerField(null=True, blank=True, choices=RETURN_TYPE_CHOICE, verbose_name="还款方式")#// 还款方式
    paymentScheduleId = models.ForeignKey(PaymentSchedule, null=True,related_name='PaymentScheduleDetails', verbose_name=u"借款标", on_delete=models.CASCADE) # // 所属还款计划
    borrower = models.ForeignKey(Borrower,null=True, verbose_name=u"还款人",related_name='PaymentScheduleDetails', on_delete=models.CASCADE)  # ;fromLogininfo; // 还款人(即发标人) borrowUser
    investor = models.ForeignKey(Investor,null=True, verbose_name=u"收款人",related_name='PaymentScheduleDetails', on_delete=models.CASCADE)  # // 收款人(即投标人) toLogininfoId
    class Meta:
        verbose_name = u"投资人的回款明细"
        verbose_name_plural = verbose_name

class UserBanknInfo(models.Model):
    bankName = models.CharField(max_length=50,blank=True, null=True, verbose_name="银行名称") #// 银行名称
    accountName = models.CharField(max_length=50,blank=True, null=True, verbose_name="开户人姓名")# // 开户人姓名
    accountNumber = models.CharField(max_length=50,blank=True, null=True, verbose_name="银行账号") #// 银行账号
    bankForkName = models.CharField(max_length=50,blank=True, null=True, verbose_name="开户支行") # // 开户支行I
    userProfile = models.ForeignKey(UserProfile,null=True, verbose_name=u"用户",related_name='userBanknInfos', on_delete=models.CASCADE)  # // 收款人(即投标人) toLogininfoId
    class Meta:
        verbose_name = u"用户银行卡"
        verbose_name_plural = verbose_name

class MoneyWithdraw(BaseAudit):
    moneyAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="提现金额")# // 提现金额
    charge = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="提现手续费") #// 提现手续费
    bankName = models.CharField(max_length=50, blank=True, null=True, verbose_name="银行名称")  # // 银行名称
    accountName = models.CharField(max_length=50, blank=True, null=True, verbose_name="开户人姓名")  # // 开户人姓名
    accountNumber = models.CharField(max_length=50, blank=True, null=True, verbose_name="银行账号")  # // 银行账号
    bankForkName = models.CharField(max_length=50, blank=True, null=True, verbose_name="开户支行")  # // 开户支行I
    class Meta:
        verbose_name = u"提现审核"
        verbose_name_plural = verbose_name


