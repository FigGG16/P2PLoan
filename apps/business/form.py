from .models import BidRequest,BidRequestAuditHistory, RechargeOffline,PlatformBankInfo,Bid, AccountFlow
from django import forms
from utils.BidConst import BidConst
from utils.CalculateUtil import CalculatetUtil
from utils.bitStatesUtils import BitStatesUtils
from django.utils import timezone
from decimal import *
class BidRequestForm(forms.ModelForm):
    class Meta:
        model = BidRequest
        fields = ['bidRequestAmount','bidRequestAmount','currentRate','monthes2Return','returnType','minBidAmount','disableDays','title','description']


    def save(self, user):
        bid_request = super(BidRequestForm, self).save(commit=False)
        bid_request.bidRequestType = BidConst.GET_BIDREQUEST_TYPE_NORMAL()
        bid_request.createUser = user.get_borrower()
        bid_request.totalRewardAmount = CalculatetUtil.calTotalInterest(self.cleaned_data.get('returnType'),
                                                                      self.cleaned_data.get('bidRequestAmount'),
                                                                      self.cleaned_data.get('currentRate'),
                                                                      self.cleaned_data.get('monthes2Return'))
        #保存
        bid_request.save()

        #给用户 添加一个状态码
        user.addState(BitStatesUtils.GET_OP_HAS_BIDREQUEST_PROCESS())
        user.save()

        #创建标的审核对象
        bid_request_auditHistory = BidRequestAuditHistory.objects.create(bidRequestId=bid_request)
        bid_request_auditHistory.applier = user
        bid_request_auditHistory.save()

        return bid_request


class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ['actualRate','availableAmount','bidRequestId','bidRequestTitle','bidUser','bidTime']

    def save(self,user, bid_request,loaner_bid_amount,commit=False):
        bid = super(BidForm, self).save(commit=False)
        bid.actualRate = bid_request.currentRate
        bid.availableAmount = Decimal(loaner_bid_amount)
        bid.bidRequestId = bid_request
        bid.bidRequestTitle = bid_request.title
        bid.bidUser = user.get_investor()
        bid.bidTime = timezone.now()
        bid.save()
        return bid



class RechargeOfflineForm(forms.ModelForm):
    class Meta:
        model = RechargeOffline
        fields = ['tradeCode', 'amount','tradeTime','note']

    def save(self, user):
        recharge_obj = super(RechargeOfflineForm, self).save(commit=False)
        platform_bank_info_obj= PlatformBankInfo.objects.get(accountNumber=self.data.get('bankAccountNumber'))
        recharge_obj.bankInfo = platform_bank_info_obj
        recharge_obj.applier = user
        recharge_obj.save()
        return recharge_obj


class AccountFlowForm(forms.ModelForm):
    class Meta:
        model = AccountFlow
        fields = ['accountId','amount','tradeTime','accountType','usableAmount','freezedAmount','note']

    def save(self,user, bid_request,loaner_account, loaner_bid_amount,commit=False):
        account_flow = super(AccountFlowForm, self).save(commit=False)
        account_flow.accountId = loaner_account
        account_flow.amount = loaner_bid_amount
        account_flow.tradeTime = timezone.now()
        account_flow.accountType = BidConst.GET_ACCOUNT_ACTIONTYPE_BID_SUCCESSFUL()
        account_flow.usableAmount = loaner_account.usableAmount
        account_flow.freezedAmount = loaner_account.freezedAmount
        account_flow.note = '投标成功，投标金额：'+str(loaner_bid_amount)
        account_flow.save()
        return account_flow
