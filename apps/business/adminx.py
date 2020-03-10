import xadmin
from .models import BidRequestAuditHistory, FullAuditOne, FullAuditTwo, BidRequest, PlatformBankInfo, RechargeOffline,AccountFlow ,\
    BidRequestAuditHistory,PublishBidAaudit,SystemAccount,SystemAccountFlow,PaymentSchedule, PaymentScheduleDetail
from django.utils import timezone
from utils.BidConst import BidConst
from utils.CalculateUtil import CalculatetUtil
from utils.DecimalFormatUtil import DecimalFormatUtil
from django.db.models import Q, Sum
from utils.bitStatesUtils import BitStatesUtils
from users.models import Account
from decimal import *
# from datetime import *
from dateutil.relativedelta import *

class BidRequestAdmin(object):
    list_display = ['createUser', 'applyTime', 'currentSum', 'returnType', 'minBidAmount', 'bidRequestState']


#所有标的审核历史
class BidRequestAuditHistoryAdmin(object):
    list_display = ['applyTime', 'bidRequestId', 'applier', 'auditType','remark', 'state','audiTime', 'auditor']

#发表前审核
class PublishBidAauditAdmin(object):
    list_display = ['applyTime', 'bidRequestId', 'applier', 'auditType','remark', 'state']
    readonly_fields = ['applier', 'bidRequestId','applyTime', 'auditType']
    exclude = ['audiTime','auditor','auditor',]
    #未审核或者审核失败
    def queryset(self):
        qs = super(PublishBidAauditAdmin, self).queryset()
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
            user_profile_obj = bid_audit.applier
            #如果审核成功
            if bid_audit.state == BitStatesUtils.STATE_AUDIT():
                #给标添加状态信息
                bid_request = bid_audit.bidRequestId
                bid_request.bidRequestState = BidConst.GET_BIDREQUEST_STATE_BIDDING()
                bid_request.note = bid_audit.remark
                #保存模型
                bid_request.save()

                #给申请用户添加借款标状态
                user_profile_obj.addState(BitStatesUtils.GET_OP_HAS_BIDREQUEST_PROCESS())
            else:
                #审核失败，移出用户招标状态
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
                bid_request.bidRequestState = BidConst.GET_BIDREQUEST_STATE_APPROVE_PENDING_2() #满标二审状态
                bid_request.note = bid_audit.remark
                #添加满标二审历史
                self.createBrAuditHistory(bid_request)
            elif bid_audit.state == BitStatesUtils.STATE_REJECT():
                #审核失败，修改借款状态
                bid_request.bidRequestState = BidConst.GET_BIDREQUEST_STATE_REJECTED() #满标审核拒绝
                #进行退款
                self.retureMoney(bid_request)
                #移出借款人借款状态码
                bid_request.createUser.userProfile.removeState(BitStatesUtils.GET_OP_HAS_BIDREQUEST_PROCESS())
                bid_request.createUser.userProfile.save()

            #保存模型
            bid_request.save()
            bid_audit.save()

    #添加满标一审状态
    def createBrAuditHistory(self, bid_request):
        bid_request_auditHistory = BidRequestAuditHistory.objects.create(bidRequestId=bid_request)
        bid_request_auditHistory.applier = bid_request.createUser.userProfile
        bid_request_auditHistory.auditType = bid_request_auditHistory.FULL_AUDIT_2
        bid_request_auditHistory.save()

    def retureMoney(self, br):
        bids = br.bids.values_list('bidUser')
        #取出所有投标用户id, 并去重
        bid_user_ids = list(set((list(zip(*bids)))[0]))
        for bid_user_id in bid_user_ids:
            #获取相同投资人投的标数量
            temp_query = br.bids.filter(bidUser_id=bid_user_id)
            #统计投资金额
            available_amount_total = temp_query.aggregate(Sum('availableAmount'))
            #获取投资人账户
            investor_account = Account.objects.get(userProfile=temp_query.first().bidUser.userProfile)
            #可用余额增加
            investor_account.usableAmount = investor_account.usableAmount + available_amount_total['availableAmount__sum']
            #冻结余额减少
            investor_account.freezedAmount = investor_account.freezedAmount - available_amount_total['availableAmount__sum']
            investor_account.save()
            #投标流水
            self.generateRetureMoneyFlow(investor_account=investor_account,br=br,available_amount_total=available_amount_total['availableAmount__sum'])

    def generateRetureMoneyFlow(self, investor_account,br, available_amount_total):
            account_flow = AccountFlow.objects.create(accountId=investor_account)
            account_flow.amount = available_amount_total
            account_flow.tradeTime = timezone.now()
            account_flow.accountType = BidConst.GET_ACCOUNT_ACTIONTYPE_BID_UNFREEZED()
            account_flow.usableAmount = investor_account.usableAmount
            account_flow.freezedAmount = investor_account.freezedAmount
            account_flow.note = "投标" +br.title + '一审失败，退款投标金额：' + str(available_amount_total)
            account_flow.save()



#满标二审
class FullAuditTwoAdmin(object):
    list_display = ['bidRequestId','auditType','applyTime','remark', 'state']
    readonly_fields = ['applier', 'applyTime', 'auditType']
    def queryset(self):
        qs = super(FullAuditTwoAdmin, self).queryset()
        qs = qs.filter(Q(auditType=BidRequestAuditHistory.FULL_AUDIT_2)&Q(state=BitStatesUtils.STATE_NORMAL()))
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
            user_profile_obj = bid_audit.applier
            #如果审核成功
            if bid_audit.state == BitStatesUtils.STATE_AUDIT():
                # // 1, 对借款要做什么事情?
                # // ** 1.1
                # 修改借款状态(还款中)
                bid_request.bidRequestState = BidConst.GET_BIDREQUEST_STATE_PAYING_BACK() #还款状态
                bid_request.note = bid_audit.remark
                #添加满标二审历史
                self.createBrAuditHistory(bid_request)

                # // 2, 对借款人要做什么事情?
                # // ** 2.1
                # 借款人收款操作
                borrow_account = Account.objects.get(userProfile=bid_request.createUser.userProfile)
                # // ** *2.1.1 账户余额增加,
                borrow_account.usableAmount = borrow_account.usableAmount + bid_request.bidRequestAmount
                # // ** *2.1.2生成收款流水;
                self.generateBorrowSuccessFlow(borrow_account=borrow_account,br=bid_request)
                # // ** *2.1.3修改待还本息;
                borrow_account.unReturnAmount = borrow_account.unReturnAmount + bid_request.bidRequestAmount + bid_request.totalRewardAmount
                # // ** *2.1.4修改可用信用额度;
                borrow_account.remainBorrowLimit = borrow_account.remainBorrowLimit - bid_request.bidRequestAmount
                # // ** 2.2移除借款人借款进行中状态码;
                bid_request.createUser.userProfile.removeState(BitStatesUtils.GET_OP_HAS_BIDREQUEST_PROCESS())
                bid_request.createUser.userProfile.save()
                # // ** 2.3支付借款手续费计算
                manage_charge_fee = CalculatetUtil.calAccountManagementCharge(bid_request.bidRequestAmount)
                # // ** *2.3.1可用余额减少
                borrow_account.usableAmount = borrow_account.usableAmount - manage_charge_fee
                # // ** *2.3.2生成支付借款手续费流水;
                self.generateBorrowChargeFeeFlow(borrow_account=borrow_account,br=bid_request,manageChargeFee=manage_charge_fee)
                # // ** *2.3.3平台收取借款手续费;
                self.systemReceiveChargeFeeFromBorrow(br=bid_request,manage_charge_fee=manage_charge_fee)

                # // 3, 对投资人要做什么事情?
                # // ** 3.1遍历投标;
                bids = bid_request.bids.values_list('bidUser')
                # 取出所有投标用户id, 并去重
                bid_user_ids = list(set((list(zip(*bids)))[0]))
                # // 汇总利息, 用于最后一个投标的用户的利息计算
                totalBidInterest = Decimal('0')
                for idx, bid_user_id in enumerate(bid_user_ids):
                    #获取投资人
                    bids_temp_query = bid_request.bids.filter(bidUser_id=bid_user_id)
                    # 获取相同投资人投的标数量
                    # 统计投资金额
                    available_amount_total = bids_temp_query.aggregate(Sum('availableAmount'))
                    # 获取投资人账户
                    investor_account = Account.objects.get(userProfile=bids_temp_query.first().bidUser.userProfile)
                    # 冻结余额减少
                    investor_account.freezedAmount = investor_account.freezedAmount - available_amount_total['availableAmount__sum']
                    # // ** 3.3生成成功投标流水
                    self.bidSuccessFlow(bid=bids_temp_query.first(),account=investor_account, total_bid_amount=available_amount_total['availableAmount__sum'])
                     # // ** 3.4计算待收利息和待收本金
                    # // ** 3.4.1待收本金
                    investor_account.unReceivePrincipal = investor_account.unReceivePrincipal + available_amount_total['availableAmount__sum']
                    #临时利息变量
                    bidInterest = Decimal('0')
                    # // ** 3.4.2待收利息
                    # // 待收利息 = 投标金额 / 借款总金额 * 借款总回报利息
                    # // 如果当前投标是整个投标列表中的最后一个投标;这个投标的利息 = 借款总回报利息 - 累加的投标利息
                    if idx == len(bid_user_ids) - 1:
                        #计算最后投标人的利息
                        bidInterest = bid_request.totalRewardAmount - totalBidInterest
                    else:
                        bidInterest = (available_amount_total['availableAmount__sum'] / bid_request.bidRequestAmount) * bid_request.totalRewardAmount
                        bidInterest =  DecimalFormatUtil.formatBigDecimal(bidInterest, BidConst.STORE_SCALE())
                        #累加总的利息 用于最后利息的计算
                        totalBidInterest = totalBidInterest + bidInterest
                    investor_account.unReceiveInterest = investor_account.unReceiveInterest + bidInterest
                    investor_account.save()
            # // 4, 思考满标二审之后的流程(还款)对满标二审有什么影响
            # // ** 4生成还款对象和回款对象
                self.createPaymentSchedules(bid_request)
            elif bid_audit.state == BitStatesUtils.STATE_REJECT():
                #审核失败，修改借款状态
                bid_request.bidRequestState = BidConst.GET_BIDREQUEST_STATE_REJECTED() #满标审核拒绝
                #进行退款
                self.retureMoney(bid_request)
                # 审核失败，移出用户招标状态
                bid_request.createUser.userProfile.removeState(BitStatesUtils.GET_OP_HAS_BIDREQUEST_PROCESS())
                bid_request.createUser.userProfile.save()
            #保存模型
            bid_request.save()
            bid_audit.save()

    # / **
    # *创建还款计划对象
    # *
    # * @ param
    # br
    # * /

    def createPaymentSchedules(self, br):
        print("timezone.now():", timezone.now())
        print("timezone.now()nextMonth:", timezone.now() + relativedelta(months=+1))
        now = timezone.now()
        # // 汇总利息和本金, 用于最后一个投标的用户的利息和本金计算
        totalInterest = Decimal('0')
        totalPrincipal = Decimal('0')
        for i in range(0, br.monthes2Return):
            payment_schedule = PaymentSchedule.objects.create(bidRequestId=br)
            # payment_schedule = PaymentSchedule(bidRequestId=br)
            payment_schedule.bidRequestTitle = br.title
            payment_schedule.bidRequestType = br.bidRequestType
            payment_schedule.borrower = br.createUser
            payment_schedule.deadLine = now + relativedelta(months=+(i+1))

            if i < (br.monthes2Return - 1):
                # // 计算这一期的总还款金额
                payment_schedule.totalAmount = CalculatetUtil.calMonthToReturnMoney(
                    returnType=br.returnType, bidRequestAmount=br.bidRequestAmount, yearRate=br.currentRate, monthIndex=i + 1, monthes2Return=br.monthes2Return
                )
                # // 计算这一期的利息
                payment_schedule.interest = CalculatetUtil.calMonthlyInterest(
                    returnType=br.returnType, bidRequestAmount=br.bidRequestAmount, yearRate=br.currentRate, monthIndex=i + 1, monthes2Return=br.monthes2Return
                )
                # // 计算这一期的本金
                payment_schedule.principal = payment_schedule.totalAmount - payment_schedule.interest
                totalInterest = totalInterest + payment_schedule.interest
                totalPrincipal = totalPrincipal + payment_schedule.principal
            else:
                # //这一期的利息
                payment_schedule.interest = br.totalRewardAmount - totalInterest
                payment_schedule.principal = br.bidRequestAmount - totalPrincipal
                payment_schedule.totalAmount = payment_schedule.principal + payment_schedule.interest

            payment_schedule.monthIndex = i + 1
            payment_schedule.returnType = br.returnType
            # // 处于待还状态
            payment_schedule.state = BidConst.GET_PAYMENT_STATE_NORMAL()
            payment_schedule.save()

            # // 生成还款明细
            self.createPaymentScheduleDetail(payment_schedule=payment_schedule,br=br)

    def createPaymentScheduleDetail(self,payment_schedule, br):
        bids = br.bids.values_list('bidUser')
        # 取出所有投标用户id, 并去重
        bid_user_ids = list(set((list(zip(*bids)))[0]))

        # // 汇总利息和本金, 用于最后一个投标的用户的利息和本金计算
        total_amount = Decimal('0')
        for idx, bid_user_id in enumerate(bid_user_ids):
            # 获取所有投资人
            bids_temp_query = br.bids.filter(bidUser_id=bid_user_id)
            #获取单个投资人
            bid = bids_temp_query.first()
            # 获取相同投资人投的标数量
            # 统计投资金额
            available_amount_total = bids_temp_query.aggregate(Sum('availableAmount'))
            payment_schedule_detail = PaymentScheduleDetail.objects.create(bidId=bid)
            payment_schedule_detail.bidAmount = available_amount_total['availableAmount__sum']
            payment_schedule_detail.bidRequestId = br
            payment_schedule_detail.deadline = payment_schedule.deadLine
            #还款人
            payment_schedule_detail.borrower = br.createUser
            if idx == len(bid_user_ids) - 1:
                payment_schedule_detail.totalAmount = payment_schedule.totalAmount - total_amount
                # // 计算利息
                interest = DecimalFormatUtil.formatBigDecimal(
                    data=(available_amount_total['availableAmount__sum'] / br.bidRequestAmount) * payment_schedule.interest,
                    scal=BidConst.STORE_SCALE()
                )
                payment_schedule_detail.interest = interest
                payment_schedule_detail.principal = payment_schedule_detail.totalAmount - payment_schedule_detail.interest

            else:
                # // 计算利息
                interest = DecimalFormatUtil.formatBigDecimal(
                    data=(available_amount_total['availableAmount__sum'] / br.bidRequestAmount) * payment_schedule.interest,
                    scal=BidConst.STORE_SCALE()
                )

                # // 计算本金
                principal = DecimalFormatUtil.formatBigDecimal(
                    data=(available_amount_total['availableAmount__sum'] / br.bidRequestAmount) * payment_schedule.principal,
                    scal=BidConst.STORE_SCALE()
                )
                payment_schedule_detail.interest=interest
                payment_schedule_detail.principal = principal
                payment_schedule_detail.totalAmount = interest + principal
                total_amount = total_amount + payment_schedule_detail.totalAmount

            payment_schedule_detail.monthIndex = payment_schedule.monthIndex
            payment_schedule_detail.paymentScheduleId = payment_schedule
            #//投资人
            payment_schedule_detail.investor = bid.bidUser
            payment_schedule_detail.save()


    def retureMoney(self, br):
        bids = br.bids.values_list('bidUser')
        #取出所有投标用户id, 并去重
        bid_user_ids = list(set((list(zip(*bids)))[0]))
        for bid_user_id in bid_user_ids:
            #获取相同投资人投的标数量
            temp_query = br.bids.filter(bidUser_id=bid_user_id)
            #统计投资金额
            available_amount_total = temp_query.aggregate(Sum('availableAmount'))
            #获取投资人账户
            investor_account = Account.objects.get(userProfile=temp_query.first().bidUser.userProfile)
            #可用余额增加
            investor_account.usableAmount = investor_account.usableAmount + available_amount_total['availableAmount__sum']
            #冻结余额减少
            investor_account.freezedAmount = investor_account.freezedAmount - available_amount_total['availableAmount__sum']
            investor_account.save()
            #投标流水
            self.generateRetureMoneyFlow(investor_account=investor_account,br=br,available_amount_total=available_amount_total['availableAmount__sum'])

    def bidSuccessFlow(self,bid, account,total_bid_amount):
        account_flow = AccountFlow.objects.create(accountId=account)
        account_flow.amount = total_bid_amount
        account_flow.tradeTime = timezone.now()
        account_flow.accountType = BidConst.GET_ACCOUNT_ACTIONTYPE_BID_SUCCESSFUL()
        account_flow.usableAmount = account.usableAmount
        account_flow.freezedAmount = account.freezedAmount
        account_flow.note = "投标" +bid.bidRequestTitle + '成功，取消投标冻结金额:' + str(total_bid_amount)
        account_flow.save()


    def generateRetureMoneyFlow(self, investor_account,br, available_amount_total):
            account_flow = AccountFlow.objects.create(accountId=investor_account)
            account_flow.amount = available_amount_total
            account_flow.tradeTime = timezone.now()
            account_flow.accountType = BidConst.GET_ACCOUNT_ACTIONTYPE_BID_UNFREEZED()
            account_flow.usableAmount = investor_account.usableAmount
            account_flow.freezedAmount = investor_account.freezedAmount
            account_flow.note = "投标" +br.title + '二审失败，退款投标金额：' + str(available_amount_total)
            account_flow.save()

    def systemReceiveChargeFeeFromBorrow(self,br,manage_charge_fee):
        # // 1, 得到当前系统账户;
        system_account = SystemAccount.objects.first()
        # // 2, 修改账户余额;
        system_account.usableAmount = system_account.usableAmount +manage_charge_fee
        system_account.save()
        # // 3, 生成收款流水
        flow = SystemAccountFlow.objects.create(systemAccountId=system_account)
        flow.accountActionType = BidConst.GET_SYSTEM_ACCOUNT_ACTIONTYPE_MANAGE_CHARGE()
        flow.amount = manage_charge_fee
        flow.usableAmount = system_account.usableAmount
        flow.freezedAmount = system_account.freezedAmount
        flow.note = "借款" +br.title + '成功，收取手续费：' + str(manage_charge_fee)
        flow.save()


    def generateBorrowSuccessFlow(self, borrow_account,br):
            account_flow = AccountFlow.objects.create(accountId=borrow_account)
            account_flow.amount = br.bidRequestAmount
            account_flow.tradeTime = timezone.now()
            account_flow.accountType = BidConst.GET_ACCOUNT_ACTIONTYPE_BIDREQUEST_SUCCESSFUL()
            account_flow.usableAmount = borrow_account.usableAmount
            account_flow.freezedAmount = borrow_account.freezedAmount
            account_flow.note = "借款" +br.title + '成功，获得金额：' + str(br.bidRequestAmount) # '借款成功，收到借款金额：' + str(all_amount)
            account_flow.save()

    def generateBorrowChargeFeeFlow(self, borrow_account, br, manageChargeFee):
        account_flow = AccountFlow.objects.create(accountId=borrow_account)
        account_flow.amount = br.bidRequestAmount
        account_flow.tradeTime = timezone.now()
        account_flow.accountType = BidConst.GET_ACCOUNT_ACTIONTYPE_CHARGE()
        account_flow.usableAmount = borrow_account.usableAmount
        account_flow.freezedAmount = borrow_account.freezedAmount
        account_flow.note = "借款" + br.title + '支付手续费成功，扣除金额：' + str(manageChargeFee)  # '借款成功，收到借款金额：' + str(all_amount)
        account_flow.save()


    # 添加满标二审通过状态
    def createBrAuditHistory(self, bid_request):
        bid_request_auditHistory = BidRequestAuditHistory.objects.create(bidRequestId=bid_request)
        bid_request_auditHistory.applier = bid_request.createUser.userProfile
        bid_request_auditHistory.auditType = bid_request_auditHistory.FULL_AUDIT_2
        bid_request_auditHistory.save()


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


class SystemAccountAdmin(object):
    list_display = ['usableAmount','freezedAmount']




xadmin.site.register(BidRequestAuditHistory,BidRequestAuditHistoryAdmin)
xadmin.site.register(PublishBidAaudit, PublishBidAauditAdmin)
xadmin.site.register(FullAuditOne, FullAuditOneAdmin)
xadmin.site.register(FullAuditTwo, FullAuditTwoAdmin)
xadmin.site.register(BidRequest, BidRequestAdmin)
xadmin.site.register(PlatformBankInfo,PlatformBankInfoAdmin)
xadmin.site.register(RechargeOffline,RechargeOfflineAdmin)
xadmin.site.register(AccountFlow,AccountFlowAdmin)
xadmin.site.register(SystemAccount,SystemAccountAdmin)