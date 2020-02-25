from django.shortcuts import render
from django.views.generic.base import View
from .models import BidRequest
from users.models import UserProfile, Account
from utils.BidConst import BidConst
from .form import BidRequestForm
from django.http import HttpResponse
# Create your views here.


class BorrowTypeList(View):
    def get(self, request):
        return render(request, "borrow_type_list.html", )


class BidRequest(View):
    def get(self, request):

        #其它条件要求留到后面完善，
        user_obj = request.user
        #当前有标正在进行 /实名认证 /绑定银行卡 / 认证分数
        if user_obj.isRealAuth() and user_obj.isCheckInBasicInfo() \
                and user_obj.isVedioAuth() and user_obj.isHasBidRequestProcess() \
                and user_obj.isBindBankInfo() and (user_obj.getScore() >= BidConst.BASE_BORROW_SCORE()):
            return render(request, "check_in_bid.html", )

        return render(request, "ban_bid.html", )


class Apply(View):
    def POST(self,request):
        account_query = Account.objects.filter(user_profile=request.user)
        if account_query.exists():
            account_obj = account_query.first()  # 系统最小借款金额 <= 借款金额 <=剩余信用额度, #5<= 利息 <=20,  #最小投标金额>=系统最小投标金额
            if account_obj.getRemainBorrowLimit() >= request.POST.get("bidRequestAmount", "") >= BidConst.SMALLEST_BID_AMOUNT() \
                and BidConst.MAX_CURRENT_RATE() >= request.POST.get("currentRate", "") >= BidConst.SMALLEST_CURRENT_RATE() \
                and request.POST.get("currentRate", "minBidAmount") >= BidConst.SMALLEST_BID_AMOUNT():

                form = BidRequestForm(request.POST)
                if form.is_valid():
                    form.save(request.user)
        # 判断是否满足条件



        return HttpResponse('{"status":"请求失败"}', content_type='application/json')









