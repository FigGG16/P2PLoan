from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import RealAuth, UserFile
from .forms import ReturnRealAuthImageForm, RealAuthForm, UserFileForm, UserFileTypeForm
from users.models import UserProfile
from .Serializers import RealAuthSerializer, UserFileSerializer
from rest_framework.response import Response


from django.db.models import Q

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
