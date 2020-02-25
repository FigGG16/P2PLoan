from django.db import models

# Create your models here.
from utils.BidConst import BidConst
from users.models import Borrower, Investor


class BidRequest(models.Model):

    RETURN_TYPE_CHOICE =(
        (0, "按月分期还款"),
        (1, "按月到期还款")
    )
    BID_REQUEST_TYPE_CHOICE = (
        (0, "普通信用标")
    )
    returnType = models.IntegerField(null=True, blank=True, choices=RETURN_TYPE_CHOICE, verbose_name="还款类型(等额本息)")
    bidRequestType = models.IntegerField(null=True, blank=True, choices=BID_REQUEST_TYPE_CHOICE, verbose_name="借款类型(信用标)")
    bidRequestState = models.IntegerField(null=True, blank=True, verbose_name="借款状态")
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
    applyTime = models.DateTimeField(auto_now_add=True, verbose_name=u"这个标的申请时间")#// 申请时间
    #
    publishTime = models.DateTimeField(blank=True,null=True, verbose_name=u"发标时间")# #// 发标时间

    class Meta:
        verbose_name = u"借款对象表"
        verbose_name_plural = verbose_name

class Bid(models.Model):

    actualRate = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(), verbose_name="年化利率")#// (等同于bidrequest上的currentRate)
    availableAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(), verbose_name="这次投标金额")# // 这次投标金额
    bidRequestId = models.ForeignKey(BidRequest, verbose_name=u"借款标来源", on_delete=models.CASCADE)#// 关联借款 来自于哪个借款标
    bidRequestTitle = models.CharField(max_length=50,blank=True, null=True, verbose_name="借款标题")#// 冗余数据, 等同于借款标题
    bidUser = models.ForeignKey(Investor, verbose_name=u"投标人", on_delete=models.CASCADE)#// 借款人#// 投标人
    bidTime = models.DateTimeField(blank=True,null=True, verbose_name=u"投标时间")#// 投标时间
    class Meta:
        verbose_name = u"一次投资对象表"
        verbose_name_plural = verbose_name
    # bidRequestState #// 不保存到数据库中, 只供查询使用