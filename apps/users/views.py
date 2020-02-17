from django.shortcuts import render
import  json
import os
from P2PLoan.settings import BASE_DIR

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from .models import Banner, EmailVerifyRecord, UserProfile, Borrower, Investor, Picture, UsersFamilyAuthentication
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, LoginRequiredMixin, UploadImageForm, \
    UserBasicProfile, UserEmploymentDetail, UserFamilyCondition, EmploymentDetail, UploadFamilyAuthenticationImageForm
from apps.utils.email_send import send_register_email

from django.views.generic import ListView, CreateView, DeleteView
from .serialize import serialize
from .response import JSONResponse, response_mimetype
# Create your views here.

from certification.forms import ReturnRealAuthImageForm


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
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg":"用户未激活！", "login_form":login_form})
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

            # if user_borrower:
            #     global user_profile
            #     user_profile.is_borrower = True
            #     borrower = Borrower.objects.create(userProfile=user_profile)
            # else:
            #     global user_profile
            #     user_profile.is_investor = True
            #     investor = Investor.objects.create(user_profile=user_profile)



            # #写入欢迎注册消息
            # user_message = UserMessage()
            # user_message.user = user_profile.id
            # user_message.message = "欢迎注册慕学在线网"
            # user_message.save()

            # send_register_email(user_name, "register")
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
        return render(request, 'borrow_home_page.html', {'form': form})

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
            user_profile.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


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
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_family_form.errors), content_type='application/json')


# 异步保存公司详细信息
class UserCompanyProfileView(LoginRequiredMixin, View):
    """
    用户基本个人信息
    """
    def get(self, request):
        return render(request, 'borrow_home_page.html')

    def post(self, request):
        employment_detail = EmploymentDetail.objects.get(borrower_id=request.user.id)
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
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_employment_form.errors), content_type='application/json')



# class UploadUserAuthenticationView(View):
#     """
#     上传用户基本信息
#     """
#     def get(self, request):
#         return render(request, 'authentication.html')
#
#     def post(self, request):
#
#         family_authentication_object = UsersFamilyAuthentication.objects.filter(user_profile_id=request.user.id)
#         if len(family_authentication_object) > 0:
#             user_authentication_image_form = UploadFamilyAuthenticationImageForm(request.POST, request.FILES, instance=family_authentication_object.first())
#         else:
#             family_authentication_object = UsersFamilyAuthentication.objects.create(user_profile_id=request.user.id)
#             user_authentication_image_form = UploadFamilyAuthenticationImageForm(request.POST, request.FILES,
#                                                                                  instance=family_authentication_object)
#         if user_authentication_image_form.is_valid():
#             family_authentication_form_model = user_authentication_image_form.save()
#             files = [serialize(family_authentication_form_model)]
#             data = {'files': files}
#             response = JSONResponse(data, mimetype=response_mimetype(self.request))
#             response['Content-Disposition'] = 'inline; filename=files.json'
#             return response
#
#         data = json.dumps(user_authentication_image_form.errors)
#         return HttpResponse(content=data, status=400, content_type='application/json')






class UploadUserAuthenticationView(CreateView):
    model = UsersFamilyAuthentication
    fields = ['file']
    template_name = "authentication.html"
    def form_valid(self, form):
        self.object = form.save(self.request)
        # 保存用户外健
        self.model.save_user_profile_id(self.object, self.request.user)
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class PictureCreateView(CreateView):
    model = Picture
    fields = "__all__"
    template_name = "authentication.html"
    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')




class UploadUserAuthenticationDeleteView(DeleteView):
    model = UsersFamilyAuthentication

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class UploadUserAuthenticationListView(ListView):
    model = UsersFamilyAuthentication
    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.model.objects.filter(user_profile_id=self.request.user.id)]
        print(files)
        data = {'files': files}
        print(data)
        response = JSONResponse(data, mimetype=response_mimetype(self.request),)
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response







# class PictureListView(ListView):
#     model = Picture
#
#     def render_to_response(self, context, **response_kwargs):
#         files = [ serialize(p) for p in self.get_queryset() ]
#         data = {'files': files}
#         response = JSONResponse(data, mimetype=response_mimetype(self.request))
#         response['Content-Disposition'] = 'inline; filename=files.json'
#         return response

