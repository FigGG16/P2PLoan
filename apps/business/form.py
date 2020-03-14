from .models import BidRequest,BidRequestAuditHistory, RechargeOffline,PlatformBankInfo,Bid, AccountFlow,UserBanknInfo,MoneyWithdraw
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

    def save(self,loaner_account, loaner_bid_amount,commit=False):
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


class UserBanknInfoForm(forms.ModelForm):
    class Meta:
        model = UserBanknInfo
        exclude = ['userProfile']

    def save(self,user_profile, commit=False):
        user_bank_info = super(UserBanknInfoForm, self).save(commit=False)
        user_bank_info.userProfile = user_profile
        # 修改用户状态码
        user_profile.addState(BitStatesUtils.GET_OP_BIND_BANKINFO())
        user_profile.save()
        user_bank_info.save()
        return user_bank_info


class MoneyWithdrawViewForm(forms.ModelForm):
    class Meta:
        model = MoneyWithdraw
        fields = ['moneyAmount']

    def save(self,user_profile,account, commit=False):
        money_with_draw = super(MoneyWithdrawViewForm, self).save(commit=False)
        user_bank_info = UserBanknInfo.objects.get(userProfile=user_profile)
        money_with_draw.charge = Decimal(BidConst.MONEY_WITHDRAW_CHARGEFEE())
        money_with_draw.bankName = user_bank_info.bankForkName
        money_with_draw.accountName = user_bank_info.accountName
        money_with_draw.accountNumber = user_bank_info.accountNumber
        money_with_draw.bankForkName = user_bank_info.bankForkName
        money_with_draw.applier = user_profile
        #用户添加状态码
        user_profile.addState(BitStatesUtils.GET_HAS_MONEYWITHDRAW_PROCESS())
        user_profile.save()

        #生成提现流水
        account.usableAmount = account.usableAmount - Decimal(self.cleaned_data.get('moneyAmount'))
        account.freezedAmount = account.freezedAmount + Decimal(self.cleaned_data.get('moneyAmount'))
        self.generateMoneyWithDrawApplyFlow(account=account,money_with_draw=money_with_draw)

        account.save()
        money_with_draw.save()
        return money_with_draw

    def generateMoneyWithDrawApplyFlow(self,account, money_with_draw):
        flow=AccountFlow.objects.create(accountId=account)
        flow.accountType =BidConst.GET_ACCOUNT_ACTIONTYPE_WITHDRAW_FREEZED()
        flow.usableAmount = account.usableAmount
        flow.freezedAmount = account.freezedAmount
        flow.amount = money_with_draw.moneyAmount
        flow.note = "提现申请,冻结金额:" +str(money_with_draw.moneyAmount)
        flow.save()



