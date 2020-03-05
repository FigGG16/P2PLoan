from django.shortcuts import render
from django.views.generic.base import View
from .models import BidRequest, PlatformBankInfo, BidRequestAuditHistory
from users.models import UserProfile, Account
from utils.BidConst import BidConst
from .form import BidRequestForm, RechargeOfflineForm, BidForm, AccountFlowForm
from django.http import HttpResponse
from certification.models import UserFile, RealAuth
from django.db.models import Q
from utils.bitStatesUtils import BitStatesUtils
from decimal import *
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


class BorrowInfoView(View):
    def get(self,request):
        #页面bid, 用户详情
        bid = request.GET.get('bid')
        bid_request = BidRequest.objects.get(id=bid)
        user_profile = bid_request.createUser.userProfile
        user_files = UserFile.objects.filter(Q(applier=user_profile)&Q(state=BitStatesUtils.STATE_AUDIT()))
        user_real_authes = RealAuth.objects.filter(Q(applier=user_profile)&Q(state=BitStatesUtils.STATE_AUDIT()))

        #投标用户账户
        loan_user_account = Account.objects.get(userProfile=request.user)
        return render(request, "borrow_info.html",{'loan_user_account':loan_user_account,'bid_request':bid_request ,'user_profile':user_profile,'user_files':user_files, 'user_real_auths':user_real_authes})


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
                 account_flow.save(user=request.user, loaner_account=loaner_account,bid_request=bid_request, loaner_bid_amount=loaner_bid_amount)

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

                 print(bid_request.bids.all())




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

