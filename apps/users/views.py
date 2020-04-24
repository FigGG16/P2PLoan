from django.shortcuts import render
import  json
import os
from P2PLoan.settings import BASE_DIR

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q,Sum
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from .models import EmailVerifyRecord, UserProfile, Borrower, Investor, Account
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, LoginRequiredMixin, UploadImageForm, \
    UserBasicProfile, UserEmploymentDetail, UserFamilyCondition, EmploymentDetail, UpdateInvestorBasicProfileForm
from apps.utils.email_send import send_register_email

# Create your views here.

from certification.forms import ReturnRealAuthImageForm
from utils.bitStatesUtils import BitStatesUtils
from certification.models import UserFile
from business.models import Bid,BidRequest,PaymentSchedule,AccountFlow,SystemAccountFlow
from webnews.models import Banner,News


from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.BidConst import BidConst


User = get_user_model()

#实现邮箱账户都能够登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwars):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))

class LoginView(View):
    def get(self, request):
        login_form = RegisterForm()
        return render(request, "login.html", {'login_form':login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if not user.is_admin:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(reverse("index"))
                    else:
                        return render(request, "login.html", {"msg":"用户未激活！", "login_form":login_form})
                else:
                    return render(request, "login.html", {"msg": "管理员不能登录", "login_form": login_form})
            else:
                return render(request, "login.html", {"msg":"用户名或密码错误！", "login_form":login_form})
        else:
            return render(request, "login.html", {"login_form":login_form})

class AciveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "emailActiveFail.html")
        return render(request, "login.html")

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("userName", "")
            user_true_name = request.POST.get("trueName", "")
            user_born_date = request.POST.get("bornDate", "")
            user_email = request.POST.get("email", "")
            user_borrower = request.POST.get("borrowerCheckbox", "")
            if UserProfile.objects.filter(Q(username=user_name) | Q(email=user_email)):
                return render(request, "register.html", {"register_form":register_form, "msg":"用户已经存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_email
            user_profile.trueName = user_true_name
            user_profile.bornDate = user_born_date
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            # 保存userProfile与一对一模型关系
            def DivideUser(is_borrower_apply, user_profile_model):
                if is_borrower_apply:
                    user_profile_model.is_borrower = True
                    user_profile_model.save()
                    borrower = Borrower()
                    borrower.userProfile = user_profile_model
                    borrower.save()
                else:
                    user_profile_model.is_investor = True
                    user_profile_model.save()
                    investor = Investor()
                    investor.userProfile = user_profile_model
                    investor.save()

            DivideUser(user_borrower, user_profile)


            send_register_email(user_email, "register")


            return render(request, "emailVerifyCode.html")
        else:
            return render(request, "register.html", {"register_form":register_form})

class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetPassword.html", {"forget_form":forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")

            if not UserProfile.objects.filter(email=email):
                return render(request, "forgetPassword.html", {"forget_form":  forget_form, "msg": "邮箱未注册"})
            send_register_email(email, "forget")

            return render(request, "emailVerifyCode.html")
        else:
            return render(request, "forgetPassword.html", {"forget_form":forget_form})

class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user_name = UserProfile.objects.get(email=email).username

                return render(request, "reSetPassward.html", {"email":email, "username": user_name})
        else:
            return render(request, "emailActiveFail.html")
        return render(request, "login.html")

class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "reSetPassward.html", {"email":email, "msg":"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "reSetPassward.html", {"email": email, "modify_form": modify_form})

class PersonCenterView(View):
    def get(self, request):
        return render(request, "personal_center.html", )

class UserAccountView(LoginRequiredMixin, View):
    def get(self, request):
        form = ReturnRealAuthImageForm()
        user_file_list = UserFile.objects.filter(applier=request.user)
        return render(request, 'borrow_home_page.html', {'form': form, 'BitStatesUtils': BitStatesUtils, 'userFileObj': user_file_list})


    def post(self, request):
        return render({'form': 'nihaho'})

class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

class IndexView(View):
    #P2P在线网 首页
    def get(self, request):
        #取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        last_bids = Bid.objects.all().order_by("-bidTime")[:4]
        last_request_bids = BidRequest.objects.all().order_by("-publishTime")[:4]
        last_news = News.objects.all().order_by("-publishTime")[:10]
        return render(request, 'index.html', {
            'all_banners':all_banners,
            'last_bids':last_bids,
            'last_request_bids':last_request_bids,
            'last_news':last_news
        })

# 异步保存投资者的详细信息
class InvestorBasicProfileView(LoginRequiredMixin, View):
    """
    用户基本个人信息
    """
    def post(self, request):
        user_info_form = UpdateInvestorBasicProfileForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success", "message":"保存成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failure", "message":"保存失败"}', content_type='application/json')

# 异步保存用户的详细信息
class UserBasicProfileView(LoginRequiredMixin, View):
    """
    用户基本个人信息
    """
    def get(self, request):
        return render(request, 'borrow_home_page.html')

    def post(self, request):
        borrower = Borrower.objects.get(userProfile_id=request.user.id)
        user_info_form = UserBasicProfile(request.POST, instance=borrower)
        if user_info_form.is_valid():
            user_info_form.save()
            user_profile = UserProfile.objects.get(id=request.user.id)
            user_profile.contact_number = request.POST.get("contact_number", "")
            user_profile.qq = request.POST.get("qq", "")
            user_profile.identity_number = request.POST.get("identity_number", "")
            user_profile.addState(BitStatesUtils.GET_OP_BASIC_INFO()) #填写基本信息状态
            user_profile.save()
            return HttpResponse('{"status":"success", "message":"保存成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failure", "message":"保存失败"}', content_type='application/json')

# 异步保存用户的家庭详细信息
class UserFamilyProfileView(LoginRequiredMixin, View):
    """
    用户基本个人信息
    """
    def get(self, request):
        return render(request, 'borrow_home_page.html')

    def post(self, request):
        borrower = Borrower.objects.get(userProfile_id=request.user.id)
        user_family_form = UserFamilyCondition(request.POST, instance=borrower)
        if user_family_form.is_valid():
            path = os.path.join(BASE_DIR, 'static/json/citis.json')
            json_data = open(path)
            data1 = json.load(json_data)  # 转换json to dict
            province = "," if data1.get(request.POST.get("province", "")) is None else data1.get(request.POST.get("province", ""))
            city = "," if data1.get(request.POST.get("city", "")) is None else data1.get(request.POST.get("city", ""))
            area = "," if data1.get(request.POST.get("area", "")) is None else data1.get(request.POST.get("area", ""))
            town = "," if data1.get(request.POST.get("town", "")) is None else data1.get(request.POST.get("town", ""))
            detail_address = "," if request.POST.get("detailAddress", "") is None else request.POST.get("detailAddress", "")
            intact_address = province + city + area + town + detail_address
            borrower.family_address = intact_address.replace(',', '')
            borrower.save()
            json_data.close()
            user_family_form.save()
            return HttpResponse('{"status":"success", "message":"保存家庭详细信息成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"success", "message":"保存家庭详细信息成功"}', content_type='application/json')

# 异步保存公司详细信息
class UserCompanyProfileView(LoginRequiredMixin, View):
    """
    用户基本个人信息
    """
    def get(self, request):
        return render(request, 'borrow_home_page.html')

    def post(self, request):
        if EmploymentDetail.objects.filter(borrower_id=request.user.id).exists():
            employment_detail = EmploymentDetail.objects.get(borrower_id=request.user.id)
        else:
            employment_detail = EmploymentDetail.objects.create(borrower_id=request.user.id)
        user_employment_form = UserEmploymentDetail(request.POST, instance=employment_detail)

        if user_employment_form.is_valid():
            path = os.path.join(BASE_DIR, 'static/json/citis.json')
            json_data = open(path)
            data1 = json.load(json_data)  # 转换json to dict
            province = "," if data1.get(request.POST.get("province", "")) is None else data1.get(request.POST.get("province", ""))
            city = "," if data1.get(request.POST.get("city", "")) is None else data1.get(request.POST.get("city", ""))
            area = "," if data1.get(request.POST.get("area", "")) is None else data1.get(request.POST.get("area", ""))
            town = "," if data1.get(request.POST.get("town", "")) is None else data1.get(request.POST.get("town", ""))
            detail_address = "," if request.POST.get("company_address", "") is None else request.POST.get("company_address", "")
            intact_address = province + city + area + town + detail_address
            employment_detail.company_address = intact_address.replace(',', '')
            employment_detail.save()
            json_data.close()


            user_employment_form.save()
            return HttpResponse('{"status":"success", "message":"保存公司信息成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"success", "message":"保存公司信息失败"}', content_type='application/json')







#之定义URL分发
#分类
def generic(request, extra_context=None, template=None, number=50):

    def noneContext():
        context = {
            'bids': [],
            'bidRequests': []
        }
        return  context
    if request.user.is_authenticated:

        account = Account.objects.filter(userProfile=request.user)
        if account.exists():
            accountFlow = AccountFlow.objects.filter(accountId_id=account.first()).order_by("-tradeTime")
        else:
            accountFlow = []
        #判断借出者还是借入者
        # obj = 0;
        if not request.user.is_investor:
            obj = request.user.get_borrower()
            ps = PaymentSchedule.objects.filter(borrower=request.user.get_borrower())

            if extra_context["page_template"]==None:
                template = 'borrow_home_page.html'
            context = {
                'bids': [],
                'bidRequests': BidRequest.objects.filter(Q(createUser=request.user.get_borrower())& Q(bidRequestState=BidConst.GET_BIDREQUEST_STATE_BIDDING())),
                'paymentSchedules': ps.order_by("id"),
                'accountflows':accountFlow
            }
        else:
            obj = request.user.get_investor()
            bids = Bid.objects.filter(bidUser=obj)
            context = {
                'bids': bids.order_by("id"),
                'paymentSchedules': [],
                'accountflows': accountFlow,

            }

            #汇总用户所投的标bids
            if extra_context["page_template"]==None:
                template = 'investor_home_page.html'
            bid_request_ids = bids.values_list('bidRequestId')
            # 取出所有投标对象requestID, 并去重
            if bid_request_ids.exists():
                bid_user_ids = list(set((list(zip(*bid_request_ids)))[0]))
                context['bidRequests'] = BidRequest.objects.filter(id__in=bid_user_ids).order_by("id")[0],
            else:
                context['bidRequests'] = []

        if extra_context is not None:
            context.update(extra_context)

        #实名认证的两个按钮
        form = ReturnRealAuthImageForm()
        user_file_list = UserFile.objects.filter(applier=request.user)
        context['form']=form
        context['BitStatesUtils'] = BitStatesUtils
        context['userFileObj'] = user_file_list
        return render(request, template, context)

    login_form = RegisterForm()
    return render(request, "login.html", {'login_form': login_form})


#xadmin自定义后台界面
from xadmin.views import CommAdminView

class Chart(CommAdminView):
    def get(self, request):
        context = super().get_context()  # 这一步是关键，必须super一下继承CommAdminView里面的context，不然侧栏没有对应数据，我在这里卡了好久
        title = "统计"  # 定义面包屑变量
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面

        # 下面你可以接着写你自己的东西了，写完记得添加到context里面就可以了
        return render(request, 'charts.html', context)

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        queryset = User.objects.filter(date_joined__month='2019')  # 按月查询
        # print(queryset)
        qs_count = User.objects.all().count()
        months_labels = [str(x)+'月' for x in range(1,13)]
        user_items = [User.objects.filter(Q(date_joined__month = str(x))&Q( date_joined__year = '2019')).count() for x in range(1,13)]

        business_total_amount = [float(self.getavailable_amount_total(year='2020',month=str(x))) for x in range(1,13)]
        manage_yield_rate = [float(self.getSystemAccountFlow_amount_total(year='2020', month=str(x))) for x in range(1, 13)]

        current_investor_nums = [self.get_investor_nums(year='2020', month=str(x)) for x in range(1, 13)]
        current_borrower_nums = [self.get_borrower_nums(year='2020', month=str(x)) for x in range(1, 13)]

        data = {
                "months_labels": months_labels,
                "user_items": user_items,
                "business_total_amount":business_total_amount,
                "manage_yield_rate":manage_yield_rate,
                "current_investor_nums":current_investor_nums,
                "current_borrower_nums":current_borrower_nums,
        }
        return Response(data)

    def getavailable_amount_total(self,year,month):
        # 统计投资金额
        bid_request_query = BidRequest.objects.filter(Q(bidRequestState = BidConst.GET_BIDREQUEST_STATE_PAYING_BACK()) & Q(applyTime__month=month) & Q(applyTime__year=year))
        if bid_request_query.exists():
            available_amount_total = bid_request_query.aggregate(Sum('bidRequestAmount'))
            return available_amount_total['bidRequestAmount__sum']
        else:
            return 0
    def getSystemAccountFlow_amount_total(self,year,month):
        systemAccountFlowRuery = SystemAccountFlow.objects.filter(Q(createdTime__month=month) & Q(createdTime__year=year))
        if systemAccountFlowRuery.exists():
            available_amount_total = systemAccountFlowRuery.aggregate(Sum('amount'))
            return available_amount_total['amount__sum']
        else:
            return 0

    def get_investor_nums(self,year,month):
        # 统计借款人数
        bid_request_query = BidRequest.objects.filter((Q(bidRequestState = BidConst.GET_BIDREQUEST_STATE_PAYING_BACK())| Q(bidRequestState = BidConst.GET_BIDREQUEST_STATE_BIDDING())) & Q(applyTime__month=month) & Q(applyTime__year=year))
        if bid_request_query.exists():
            return bid_request_query.count()
        else:
            return 0

    def get_borrower_nums(self,year,month):
        # 统计投资人数
        bid_request_query = BidRequest.objects.filter(Q(bidRequestState = BidConst.GET_BIDREQUEST_STATE_PAYING_BACK()) & Q(applyTime__month=month) & Q(applyTime__year=year))

        if bid_request_query.exists():
            list_id = []
            for br in bid_request_query:
                bids = br.bids.values_list('bidUser')
                # 取出所有投标用户id, 并去重
                bid_user_ids = list(set((list(zip(*bids)))[0]))
                list_id.extend(bid_user_ids)
            list_id = list(set(list_id))

            return len(list_id)
        else:
            return 0


