import xadmin
from .models import BidRequestAuditHistory, FullAuditOne, FullAuditTwo, BidRequest, PlatformBankInfo, RechargeOffline,AccountFlow
from django.utils import timezone
from utils.BidConst import BidConst
from django.db.models import Q, Sum
from utils.bitStatesUtils import BitStatesUtils
from users.models import Account
from decimal import *

class BidRequestAdmin(object):
    list_display = ['createUser', 'applyTime', 'currentSum', 'returnType', 'minBidAmount', 'bidRequestState']


#发表前审核
class BidRequestAuditHistoryAdmin(object):
    list_display = ['applyTime', 'bidRequestId', 'applier', 'auditType','remark', 'state']
    readonly_fields = ['applier', 'bidRequestId','applyTime', 'auditType']
    exclude = ['audiTime','auditor','auditor',]
    #未审核或者审核失败
    def queryset(self):
        qs = super(BidRequestAuditHistoryAdmin, self).queryset()
        #未审核且标的申请存在
        qs = qs.filter(Q(auditType=BidRequestAuditHistory.PUBLISH_AUDIT)&Q(state=BitStatesUtils.STATE_NORMAL()))
        return qs



    # //审核表，添加审核人
    def save_models(self):
        #获取保持对象
        obj = self.new_obj
        obj.save()
        if obj is not None:
            bid_audit = obj
            bid_audit.auditor = self.user.username
            bid_audit.audiTime = timezone.now()

            #如果审核成功
            if bid_audit.state == BitStatesUtils.STATE_AUDIT():
                #给标添加状态信息
                bid_request = bid_audit.bidRequestId
                bid_request.bidRequestState = BidConst.GET_BIDREQUEST_STATE_BIDDING()
                bid_request.note = bid_audit.remark
                #保存模型
                bid_request.save()

            else:
                #审核失败，移出用户招标状态
                user_profile_obj = bid_audit.bidRequestId.createUser.userProfile
                user_profile_obj.removeState(BitStatesUtils.GET_OP_HAS_BIDREQUEST_PROCESS())
                user_profile_obj.save()

            bid_audit.save()

#满标一审
class FullAuditOneAdmin(object):
    list_display = ['bidRequestId','auditType','applyTime','remark', 'state']
    readonly_fields = ['applier', 'applyTime', 'auditType']

    def queryset(self):
        qs = super(FullAuditOneAdmin, self).queryset()
        qs = qs.filter(Q(auditType=BidRequestAuditHistory.FULL_AUDIT_1)&Q(state=BitStatesUtils.STATE_NORMAL()))
        return qs

    # //审核表，添加审核人
    def save_models(self):
        #获取保持对象
        obj = self.new_obj
        obj.save()
        if obj is not None:
            bid_audit = obj
            bid_audit.auditor = self.user.username
            bid_audit.audiTime = timezone.now()
            bid_request = bid_audit.bidRequestId
            #如果审核成功
            if bid_audit.state == BitStatesUtils.STATE_AUDIT():
                #给标添加状态信息
                bid_request.bidRequestState = BidConst.GET_BIDREQUEST_STATE_APPROVE_PENDING_1() #满标一审状态
                bid_request.note = bid_audit.remark
            elif bid_audit.state == BitStatesUtils.STATE_REJECT():
                #审核失败，修改借款状态
                bid_request.bidRequestState = BidConst.GET_BIDREQUEST_STATE_REJECTED() #满标审核拒绝
                #进行退款
                self.retureMoney(bid_request)
                #移出借款人借款状态码
                bid_request.createUser.userProfile.removeState(BitStatesUtils.GET_OP_HAS_BIDREQUEST_PROCESS())

            #保存模型
            bid_request.save()
            bid_audit.save()

    def retureMoney(self, br):
        bids = br.bids.values_list('bidUser')
        #取出所有投标用户id, 并去重
        bid_user_ids = list(set((list(zip(*bids)))[0]))
        for bid_user_id in bid_user_ids:
            #获取相同投资人投的标数量
            temp_query = br.bids.filter(bidUser_id=bid_user_id)
            #统计投资金额
            available_amount_totall = temp_query.aggregate(Sum('availableAmount'))
            #获取投资人账户
            investor_account = Account.objects.get(userProfile=temp_query.first().bidUser.userProfile)
            #可用余额增加
            investor_account.usableAmount = investor_account.usableAmount + available_amount_totall['availableAmount__sum']
            #冻结余额减少
            investor_account.freezedAmount = investor_account.freezedAmount - available_amount_totall['availableAmount__sum']
            investor_account.save()
            #投标流水
            self.generateRetureMoneyFlow(investor_account=investor_account,available_amount_totall=available_amount_totall['availableAmount__sum'])

    def generateRetureMoneyFlow(self, investor_account, available_amount_totall):
            account_flow = AccountFlow.objects.create(accountId=investor_account)
            account_flow.amount = available_amount_totall
            account_flow.tradeTime = timezone.now()
            account_flow.accountType = BidConst.GET_ACCOUNT_ACTIONTYPE_BID_UNFREEZED()
            account_flow.usableAmount = investor_account.usableAmount
            account_flow.freezedAmount = investor_account.freezedAmount
            account_flow.note = '一审失败，退款投标金额：' + str(available_amount_totall)
            account_flow.save()



#满标二审
class FullAuditTwoAdmin(object):
    list_display = ['bidRequestId','auditType','applyTime','remark', 'state']
    readonly_fields = ['applier', 'applyTime', 'auditType']
    def queryset(self):
        qs = super(FullAuditTwoAdmin, self).queryset()
        qs = qs.filter(auditType=BidRequestAuditHistory.FULL_AUDIT_2)
        return qs


#平台银行卡信息
class PlatformBankInfoAdmin(object):
    list_display =['bankName','accountName','accountNumber','bankForkName']



#账户流水
class AccountFlowAdmin(object):
    list_display = ['accountId','amount','tradeTime','accountType','usableAmount','freezedAmount','note']
    readonly_fields = ['accountId','amount','tradeTime','accountType','usableAmount','freezedAmount','note']

#在线充值
class RechargeOfflineAdmin(object):
    list_display = ['applier','bankInfo', 'tradeCode', 'applyTime','tradeTime', 'note', 'state']
    readonly_fields = ['applier','bankInfo', 'tradeCode', 'applyTime','tradeTime','amount', 'note']
    exclude = ['audiTime','auditor','auditor',]
    def queryset(self):
        qs = super(RechargeOfflineAdmin, self).queryset()
        qs = qs.filter(state=BitStatesUtils.STATE_NORMAL())
        return qs

    # //审核表，添加审核人
    def save_models(self):
        #获取保持对象
        obj = self.new_obj
        obj.save()
        if obj is not None:
            charge_obj = obj
            charge_obj.auditor = self.user.username
            charge_obj.audiTime = timezone.now()

            #如果审核成功
            if charge_obj.state == BitStatesUtils.STATE_AUDIT():
                #得到申请人的账户对象
                user_account = Account.objects.get(user_profile=charge_obj.applier)
                #增加账户可用余额
                user_account.usableAmount = user_account.usableAmount + charge_obj.amount
                user_account.save()
                #生成流水
                account_flow = AccountFlow.objects.create(accountId=user_account)#添加用户账户
                account_flow.accountType = BidConst.GET_ACCOUNT_ACTIONTYPE_RECHARGE_OFFLINE()#充值类型
                account_flow.amount = charge_obj.amount #添加变化金额
                account_flow.freezedAmount = user_account.freezedAmount #添加冻结金额
                account_flow.note = '线下充值成功，充值金额：'+str(charge_obj.amount)
                account_flow.tradeTime = timezone.now() #添加时间
                account_flow.usableAmount = user_account.usableAmount #添加可用金额
                account_flow.save()
            charge_obj.save()


xadmin.site.register(BidRequestAuditHistory, BidRequestAuditHistoryAdmin)
xadmin.site.register(FullAuditOne, FullAuditOneAdmin)
xadmin.site.register(FullAuditTwo, FullAuditTwoAdmin)
xadmin.site.register(BidRequest, BidRequestAdmin)
xadmin.site.register(PlatformBankInfo,PlatformBankInfoAdmin)
xadmin.site.register(RechargeOffline,RechargeOfflineAdmin)
xadmin.site.register(AccountFlow,AccountFlowAdmin)