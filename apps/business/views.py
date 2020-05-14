from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.list import ListView
from .models import BidRequest, PlatformBankInfo, BidRequestAuditHistory, MoneyWithdraw, PaymentSchedule, PaymentScheduleDetail, AccountFlow, SystemAccount,SystemAccountFlow
from users.models import UserProfile, Account
from utils.BidConst import BidConst
from .form import BidRequestForm, RechargeOfflineForm, BidForm, AccountFlowForm,UserBanknInfoForm,MoneyWithdrawViewForm
from django.http import HttpResponse
from certification.models import UserFile, RealAuth
from django.db.models import Q
from utils.bitStatesUtils import BitStatesUtils
from utils.CalculateUtil import CalculatetUtil
from decimal import *
from users.forms import LoginRequiredMixin
from django.utils import timezone
# Create your views here.


class BorrowTypeList(View):
    def get(self, request):

        return render(request, "borrow_type_list.html", )


class BidRequestView(View):
    def get(self, request):

        #其它条件要求留到后面完善，
        user_obj = request.user
        #当前有标正在进行 /实名认证 /绑定银行卡 / 认证分数
        if user_obj.isRealAuth() and user_obj.isCheckInBasicInfo() \
                and user_obj.isVedioAuth() and user_obj.isHasBidRequestProcess() \
                and user_obj.isBindBankInfo() and (user_obj.getScore() >= BidConst.BASE_BORROW_SCORE()):
            return render(request, "ban_bid.html", )
        return render(request, "check_in_bid.html", )

        #


class ApplyView(View):
    def post(self,request):
        # if (request.POST.get("bidRequestAmount", "") and request.POST.get("currentRate", "") and request.POST.get("minBidAmount", "")) is True:
        x = int(request.POST.get("bidRequestAmount", ""))
        y =  int(request.POST.get("currentRate", ""))
        z = int(request.POST.get("minBidAmount", ""))
        account_query = Account.objects.filter(userProfile=request.user)
        if account_query.exists():
            account_obj = account_query.first()
            # 系统最小借款金额 <= 借款金额 <=剩余信用额度, #5<= 利息 <=20,  #最小投标金额>=系统最小投标金额
            if int(account_obj.getRemainBorrowLimit()) >= int(request.POST.get("bidRequestAmount", "")) >= BidConst.SMALLEST_BID_AMOUNT()\
                and BidConst.MAX_CURRENT_RATE() >= int(request.POST.get("currentRate", "")) >= BidConst.SMALLEST_CURRENT_RATE() \
                and int(request.POST.get("minBidAmount", "")) >= BidConst.SMALLEST_BID_AMOUNT():
                form = BidRequestForm(request.POST)
                if form.is_valid():
                    form.save(request.user)
                return render(request, "succeed_bid.html", {'message': '投标成功'})
        # 判断是否满足条件
        return HttpResponse('{"status":"请求失败"}', content_type='application/json')
        # 判断是否满足条件
        # return HttpResponse('{"status":"信息填写错误"}', content_type='application/json')


class BorrowInfoView(LoginRequiredMixin,View):
    def get(self,request):
        #页面bid, 用户详情
        bid = request.GET.get('bid')
        bid_request = BidRequest.objects.get(id=bid)
        user_profile = bid_request.createUser.userProfile
        user_files = UserFile.objects.filter(Q(applier=user_profile)&Q(state=BitStatesUtils.STATE_AUDIT()))
        user_real_authes = RealAuth.objects.filter(Q(applier=user_profile)&Q(state=BitStatesUtils.STATE_AUDIT()))
        bids = bid_request.bids.all()

        #投标用户账户
        loan_user_account = Account.objects.filter(userProfile=request.user)

        #如何账户没有开通账户//转到登录



        return render(request, "borrow_info.html",{'loan_user_account':loan_user_account.first(),'bid_request':bid_request ,
                                                   'user_profile':user_profile,'user_files':user_files,
                                                   'user_real_auths':user_real_authes,'bids':bids})


class BidView(View):
    def post(self,request):
         #// 检查, 得到借款信息
         query = BidRequest.objects.filter(id=request.POST.get('bidRequestId'))

         loaner_bid_amount = Decimal(request.POST.get('amount'))
         #获取贷款款账户
         loaner_account = Account.objects.get(userProfile=request.user)

         #如何借款信息存在
         if query.exists():
             #获得借款信息对象
             bid_request = query.first()
             # 1,借款状态为招标中; 2,当前用户不是借款的借款人; 3,当前用户账户余额>=投标金额; 4,投标金额>=最小投标金额; 5,投标金额<=借款剩余投标金额;
             if bid_request.minBidAmount <= loaner_bid_amount \
                     and bid_request.bidRequestState == BidConst.GET_BIDREQUEST_STATE_BIDDING() \
                     and bid_request.createUser.userProfile.id != loaner_account.userProfile.id \
                     and loaner_account.usableAmount >= loaner_bid_amount \
                     and bid_request.getRemainAmount() >= loaner_bid_amount:
                 # // 执行投标操作
                 # // 1, 创建一个投标对象;
                 # 设置相关属性;
                 bid_form = BidForm()
                 bid_form.save(user=request.user, bid_request=bid_request,loaner_bid_amount=loaner_bid_amount)
                 #2, 得到投标人账户, 修改账户信息;
                 loaner_account.usableAmount = loaner_account.usableAmount - loaner_bid_amount
                 loaner_account.freezedAmount = loaner_account.freezedAmount + loaner_bid_amount
                 loaner_account.save()
                 #// 3,生成一条投标流水;
                 account_flow = AccountFlowForm()
                 account_flow.save(loaner_account=loaner_account, loaner_bid_amount=loaner_bid_amount)
                 # // 4, 修改借款相关信息;
                 bid_request.bidCount = bid_request.bidCount+1
                 bid_request.currentSum = bid_request.currentSum + loaner_bid_amount
                 bid_request.save()
                 #// 判断当前标是否投满:
                 if bid_request.bidRequestAmount == bid_request.currentSum:
                     # // 1, 修改标的状态;，满标一审
                     bid_request.bidRequestState = BidConst.GET_BIDREQUEST_STATE_APPROVE_PENDING_1()
                     bid_request.save()
                     #生成满标一审
                     self.createBrAuditHistory(bid_request=bid_request)
                 return HttpResponse('{"status":"success", "message":"投标成功"}', content_type='application/json')
         return HttpResponse('{"status":"failure", "message":"投标失败"}', content_type='application/json')

    def createBrAuditHistory(self, bid_request):
        bid_request_auditHistory = BidRequestAuditHistory.objects.create(bidRequestId=bid_request)
        bid_request_auditHistory.applier = bid_request.createUser.userProfile
        bid_request_auditHistory.auditType = bid_request_auditHistory.FULL_AUDIT_1
        bid_request_auditHistory.save()



class RechargeView(View):

    def get(self,request):
        all_bank_info = PlatformBankInfo.objects.all()
        return render(request, "recharge.html", {"all_bank_info":all_bank_info})


    def post(self,request):
        form = RechargeOfflineForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return render(request, "succeed_bid.html", {'message': '提交成功'})
        return render(request, "index.html", )


class BindUserBankInfoView(View):
    def post(self,request):

        if not request.user.isBindBankInfo():
            form = UserBanknInfoForm(request.POST)
            if form.is_valid():
                form.save(user_profile=request.user)
                #修改用户状态码
            return HttpResponse('{"status":"success", "message":"绑定成功"}', content_type='application/json')
        return HttpResponse('{"status":"failure", "message":"银行卡已经绑定"}', content_type='application/json')


class MoneyWithdrawView(View):
    def post(self,request):

        account = Account.objects.get(userProfile=request.user)
        without_amount = int(request.POST.get('moneyAmount'))
        #最小提现 <提现金额<最大提现，  提现金额<可提现金额
        if request.user.isBindBankInfo() and not request.user.isMoneyWithoutProcess() \
                and without_amount <= int(account.usableAmount) \
                and BidConst.MIN_WITHDRAW_AMOUNT() <= without_amount <= BidConst.MAX_WITHDRAW_AMOUNT():
            form=MoneyWithdrawViewForm(request.POST)
            if form.is_valid():
                form.save(user_profile=request.user,account=account)
                return HttpResponse('{"status":"success", "message":"提现申请成功"}', content_type='application/json')
        return HttpResponse('{"status":"failure", "message":"提现失败"}', content_type='application/json')


class BidRequestListView(ListView):

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', None)
        if filter_val == None or filter_val == '0':
            return self.queryset
        new_context =BidRequest.objects.filter(bidRequestState=int(filter_val))

        return new_context


    model = BidRequest
    template_name = 'bid_list.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'bidRequests'  # Default: object_list
    paginate_by = 4
    queryset = BidRequest.objects.all()

#还款
class DoReturnMoney(View):

    def post(self,request):
        # 获取PaymentSchedule #根据前端传进来的PaymentSchedulesID索引出还款进度
        ps = PaymentSchedule.objects.get(id=request.POST.get('PaymentSchedulesID'))
        #获取借款者账户
        borrowAccount = Account.objects.get(userProfile=request.user)
    # // 得到paymentschedule判断;
    # // ** *1, 还款对象的状态处于待还状态;
    # // ** *2, 还款的金额 <= 账户余额;
        if ps.state == BidConst.GET_PAYMENT_STATE_NORMAL() and borrowAccount.usableAmount >= ps.totalAmount:
            # // 1, 针对还款对象;
            # // ** *1.1, 修改还款对象状态;设置属性;
            ps.payDate = timezone.now()
            ps.state = BidConst.GET_PAYMENT_STATE_DONE()
            # // 2, 针对还款人;
            # // ** *2.1, 可用余额减少;生产还款流水;
            borrowAccount.usableAmount = borrowAccount.usableAmount - ps.totalAmount
            self.doReturnMoneyFlow(ps=ps, borrowAccount=borrowAccount)
            # // ** *2.2, 待还总金额减少;
            borrowAccount.unReturnAmount = borrowAccount.unReturnAmount - ps.totalAmount
            # // ** *2.2, 剩余信用额度增加;
            borrowAccount.remainBorrowLimit = borrowAccount.remainBorrowLimit + ps.principal
            # // 3, 针对收款人;
            # // ** *3.1, 遍历paymentscheduledetail;
            psds = ps.PaymentScheduleDetails.all()
            for psd in psds:
            #获取每个投资者账户
                investorAccount = Account.objects.get(userProfile=psd.investor.userProfile)
                # // ** *3.2, 投资人可用余额增加;生成收款流水;
                investorAccount.usableAmount = investorAccount.usableAmount + psd.totalAmount
                self.receiveMoneyFlow(psd=psd,account=investorAccount)
                # // ** *3.3, 减少待收利息和待收本金;
                investorAccount.unReceiveInterest = investorAccount.unReceiveInterest-psd.interest
                investorAccount.unReceivePrincipal = investorAccount.unReceivePrincipal-psd.principal
                # // ** *3.4, 支付利息管理费;生成支付流水;
                interestChargeFee = CalculatetUtil.calInterestManagerCharge(psd.interest)
                investorAccount.usableAmount = investorAccount.usableAmount - interestChargeFee
                self.interestChargeFeeFlow(psd=psd,account=investorAccount,interestChargeFee=interestChargeFee)
                # // ** *3.5, 系统账户收到利息管理费, 生成收款流水;
                self.chargeInterestFeeForSystem(psd=psd,interestChargeFee=interestChargeFee)
                psd.payDate = timezone.now()
                investorAccount.save()
                psd.save()
            ps.save()
            borrowAccount.save()
            # // 如果当前还款之后, 该借款所有还款已经全部换完
            # 遍历是否所有期都已经还清(是否为仍然为PAYMENT_STATE_NORMAL状态)，不是则表示所有还清，然后更改标的状态，否者不必理会
            currentBidRequest = ps.bidRequestId
            #如何有一个标为逾期或者还款状态，则不更新标的状态
            result = currentBidRequest.PaymentSchedules.filter(Q(state=BidConst.GET_PAYMENT_STATE_NORMAL()) | Q(state=BidConst.GET_PAYMENT_STATE_OVERDUE()))
            if not result.exists():
                currentBidRequest.bidRequestState = BidConst.GET_BIDREQUEST_STATE_COMPLETE_PAY_BACK()
                currentBidRequest.save()

            return HttpResponse('{"status":"success", "message":"还款成功"}', content_type='application/json')

        return HttpResponse('{"status":"failure", "message":"余额不足"}', content_type='application/json')

    def createBaseFlow(self,account):
        flow = AccountFlow.objects.create(accountId=account)
        flow.tradeTime = timezone.now()
        flow.usableAmount = account.usableAmount
        flow.freezedAmount = account.freezedAmount
        return  flow

    def doReturnMoneyFlow(self,ps,borrowAccount):
        flow = self.createBaseFlow(borrowAccount)
        flow.accountType = BidConst.GET_ACCOUNT_ACTIONTYPE_RETURN_MONEY()
        flow.amount = ps.totalAmount
        flow.note = "还款成功，还款金额：" + str(ps.totalAmount)
        flow.save()

    def receiveMoneyFlow(self,psd, account):
        flow = self.createBaseFlow(account=account)
        flow.accountType = BidConst.GET_ACCOUNT_ACTIONTYPE_CALLBACK_MONEY()
        flow.amount = psd.totalAmount
        flow.note = "回款成功，还款金额：" + str(psd.totalAmount)
        flow.save()

    def interestChargeFeeFlow(self,psd,interestChargeFee,account):
        flow = self.createBaseFlow(account=account)
        flow.accountType = BidConst.GET_ACCOUNT_ACTIONTYPE_INTEREST_SHARE()
        flow.amount = interestChargeFee
        flow.note = "回款成功，还款金额：" + str(psd.totalAmount) + ",支付利息管理费："+ str(interestChargeFee)
        flow.save()

    def chargeInterestFeeForSystem(self,psd, interestChargeFee):
        # // 1, 得到当前系统账户;
        systemAccount = SystemAccount.objects.first()
        # // 2, 修改账户余额;
        systemAccount.usableAmount = systemAccount.usableAmount + interestChargeFee
        # // 3, 生成收款流水
        flow = SystemAccountFlow.objects.create(systemAccountId=systemAccount)
        flow.accountActionType = BidConst.GET_SYSTEM_ACCOUNT_ACTIONTYPE_INTREST_MANAGE_CHARGE()
        flow.amount = interestChargeFee
        flow.usableAmount = systemAccount.usableAmount
        flow.createdTime = timezone.now()
        flow.freezedAmount = systemAccount.freezedAmount
        flow.note = "用户收款" + str(psd.totalAmount) + "成功,收取利息管理费:" + str(interestChargeFee)
        flow.save()


    # RETURN_TYPE_CHOICE =(
    #     (0, "按月分期还款"),
    #     (1, "按月到期还款")
    # )
    # STATE_CHOICE= (
    #     (0, "正常待还"),
    #     (1, "已还"),
    #     (2, "逾期")
    # )
    # BID_REQUEST_TYPE_CHOICE = (
    #     (0, "普通信用标"),
    #     (1, "普通信用标")
    # )
    # bidRequestId = models.ForeignKey(BidRequest,related_name='PaymentSchedules',null=True, verbose_name=u"借款标", on_delete=models.CASCADE)#; // 对应借款
    # bidRequestTitle = models.CharField(max_length=50,blank=True, null=True, verbose_name="借款名称")# // 借款名称
    # borrower = models.ForeignKey(Borrower, verbose_name=u"还款人",null=True,related_name='PaymentSchedules', on_delete=models.CASCADE)#; // 还款人
    # deadLine = models.DateTimeField(null=True, verbose_name=u"本期还款截止期限") # // 本期还款截止期限
    # payDate = models.DateTimeField(null=True, verbose_name=u"还款时间") # // 还款时间
    # totalAmount = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
    #                                     verbose_name="本期还款总金额")#// // 本期还款总金额，利息 + 本金
    # principal = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
    #                                     verbose_name="本期还款本金")#// 本期还款本金
    # interest = models.DecimalField(max_digits=18, decimal_places=BidConst.STORE_SCALE(), default=BidConst.ZERO(),
    #                                     verbose_name="本期还款总利息")# // 本期还款总利息
    # monthIndex = models.IntegerField(null=True, blank=True, verbose_name="第几期")#// 第几期(即第几个月)
    # state = BidConst.PAYMENT_STATE_NORMAL = models.IntegerField(null=True, blank=True,default=BidConst.GET_PAYMENT_STATE_NORMAL(),choices=STATE_CHOICE,verbose_name="本期还款状态")# // 本期还款状态（默认正常待还）
    # bidRequestType = models.IntegerField(null=True, blank=True, choices=BID_REQUEST_TYPE_CHOICE, verbose_name="借款类型(信用标)") #// 借款类型
    # returnType = models.IntegerField(null=True, blank=True, choices=RETURN_TYPE_CHOICE, verbose_name="还款方式")#// 还款方式，等同借款(BidRequest)

