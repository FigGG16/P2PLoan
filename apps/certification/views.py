from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from .models import RealAuth
from .forms import ReturnRealAuthImageForm, RealAuthForm, UserFileForm, UserFileTypeForm
from .Serializers import RealAuthSerializer
from random import choice
import re
from .models import VerifyCode
from P2PLoan.settings import REGEX_MOBILE
from django.contrib.auth import get_user_model
from datetime import datetime,timedelta
from utils.yunpian import YunPian
from utils.bitStatesUtils import BitStatesUtils


User = get_user_model()
# //异步存储认证图片
class RealAuthImageView(View):
    def post(self, request):
        form = ReturnRealAuthImageForm(request.POST, request.FILES)
        print(request.FILES['file'].name)
        if form.is_valid():
            # 返回已存图片url
            # //获取用户表申请记录
            real_auth_record = RealAuth.objects.filter(applier=request.user)
            # 记录不存在
            if not real_auth_record:
                # 新增表
                form.save(user=request.user)
            else:
                # 更新表单
                renew_record = real_auth_record.first()
                form = ReturnRealAuthImageForm(request.POST, request.FILES, instance=renew_record)
                form.save(user=request.user)
            # 表单序列化
            queryset_user_auth_record = RealAuth.objects.filter(applier=request.user).first()
            user_auth_record_serialize = RealAuthSerializer(queryset_user_auth_record, context={"request": request, "status": "success"})

            # //对数据进行转义：单引号变成双引号
            return HttpResponse(str(user_auth_record_serialize.data).replace("\'", '\"'), content_type='application/json')
        return HttpResponse('{"status":"请求失败"}', content_type='application/json')

class RealAuthView(View):
    def post(self, request):
        form = RealAuthForm(request.POST)
        if form.is_valid():
            real_auth_record = RealAuth.objects.filter(applier=request.user)
            # //记录存在则插入到已存在表单
            if real_auth_record.exists():
                form = RealAuthForm(request.POST, request.FILES, instance=real_auth_record.first())
                form.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse('{"status":"请求失败"}', content_type='application/json')


#用户选择图片文件后 会自动加载POST方法 file-upload插件
class UserFileUploadView(View):
    # def get(self, request):
    #     user_file_list = UserFile.objects.all()
    #     user_file_list_serialize = UserFileSerializer(user_file_list, context={"request": request, "status": "success"})
    #     # //对数据进行转义：单引号变成双引号
    #     return HttpResponse(str(user_file_list_serialize.data).replace("\'", '\"'), content_type='application/json')
    def post(self, request):
        form = UserFileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            user_file = form.save(user=request.user)
            data = {'is_valid': True, 'name': user_file.image.name, 'url': user_file.image.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


#b保存每次图片的类型
class UserFileTypeView(View):

    def post(self, request):
        form = UserFileTypeForm(self.request.POST,instance=request.user)
        if form.is_valid():
            form.save(user=request.user)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse('{"status":"fail"}', content_type='application/json')


class SendVerifyCodeView(View):

    def post(self,request):
        #进行手机验证校验
        mobile = request.POST.get('mobile')
        message = self.validate_mobile(mobile=mobile)
        #手机号码合法
        if message == "True":
            #签名
            # yun_pian = YunPian("74e1cd8035b6d8d24f8c18ebe9e10d3d")
            code = self.generate_code()
            # sms_status = yun_pian.send_sms(code=code, mobile=mobile)
            #customized
            print("验证码为：",code)
            sms_status = {'code': 0, 'msg': '发送成功', 'count': 1, 'fee': 0.05, 'unit': 'RMB', 'mobile': '13647861478', 'sid': 51949522510}
            if sms_status["code"] != 0:

                return JsonResponse({
                    "status": "failure",
                    "mobile": sms_status["mobile"],
                })

            else:
                code_record = VerifyCode(code=code, mobile=mobile)
                code_record.save()
                return JsonResponse({
                    "status": "success",
                    "mobile": sms_status["mobile"],
                })

        data = {"status":"failure","message":message}
        return JsonResponse(data)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """

        # 手机是否注册
        if User.objects.filter(contact_number=mobile).count():
            return "用户已经存在"

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            return "手机号码非法"


        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            return "距离上一次发送未超过60s"

        return "True"

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)


class AuditPhoneView(View):

    def post(self,request):
        code = request.POST.get('code')
        mobile = request.POST.get('mobile')
        message = self.validate_code(code=code,mobile=mobile)

        if message == "True":
            #给user账户添加手机号
            userProfile = request.user
            userProfile.contact_number = mobile
            #修改用户状态位
            userProfile.addState(BitStatesUtils.GET_OP_BIND_PHONE())
            userProfile.save()
            return JsonResponse({"status": "success", "message": "手机认证成功"})
        return JsonResponse({"status": "failure", "message": message})


    def validate_code(self, code, mobile):
        #查询是否存在记录并进行排序
        verify_records = VerifyCode.objects.filter(mobile=mobile).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                return "验证码过期"

            if last_record.code != code:
                return "验证码错误"
            else:
                return "True"

        else:
            return "验证码错误"
