from .models import BidRequest
from django import forms
from utils.BidConst import BidConst

class BidRequestForm(forms.ModelForm):
    class Meta:
        model = BidRequest
        fields = ['bidRequestAmount','bidRequestAmount','currentRate','monthes2Return','returnType','minBidAmount','disableDays','title','description']


    def save(self, user):
        bid_request = super(BidRequestForm, self).save(commit=False)
        bid_request.bidRequestType = BidConst.GET_BIDREQUEST_TYPE_NORMAL()
        bid_request.createUser = user

        bid_request.save()
        return bid_request




    returnType = models.IntegerField(null=True, blank=True, verbose_name="还款类型(等额本息)")
    bidRequestType = models.IntegerField(null=True, blank=True, verbose_name="借款类型(信用标)")
    bidRequestState = models.IntegerField(null=True, blank=True, verbose_name="借款状态")


    bidCount = models.IntegerField(null=True, blank=True, verbose_name="已投标次数(冗余)",default=0) #//
    totalRewardAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="总回报金额(总利息)")#// 总回报金额(总利息)
    currentSum = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
                                        verbose_name="当前已投标总金额") #// 当前已投标总金额


    #
    # bids #// 针对该借款的投标

    #
    publishTime = models.DateTimeField(blank=True,null=True, verbose_name=u"发标时间")# #// 发标时间
    # #



