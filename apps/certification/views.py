from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import RealAuth
from .forms import ReturnRealAuthImageForm, RealAuthForm
from users.models import UserProfile
from .Serializers import RealAuthSerializer
from rest_framework.response import Response

# //异步存储认证图片
class RealAuthImageView(View):
    def post(self, request):
        form = ReturnRealAuthImageForm(request.POST, request.FILES)
        print(request.FILES['file'].name)
        if form.is_valid():
            # 返回已存图片url
            image_url = "http://127.0.0.1:8010/media/image/"
            # //获取用户表申请记录

            real_auth_record = RealAuth.objects.filter(applier=request.user.username)
            # 记录不存在
            if not real_auth_record:
                # 新增表
                form.save()
            else:
                # 更新表单
                renew_record = real_auth_record.first()
                form = ReturnRealAuthImageForm(request.POST, request.FILES, instance=renew_record)
                form.save()
            # 表单序列化
            queryset_user_auth_record = RealAuth.objects.filter(applier=request.user.username).first()
            user_auth_record_serialize = RealAuthSerializer(queryset_user_auth_record, context={"request": request, "status": "success"})

            # //对数据进行转义：单引号变成双引号
            print(user_auth_record_serialize.data)
            return HttpResponse(str(user_auth_record_serialize.data).replace("\'", '\"'), content_type='application/json')
        return HttpResponse('{"status":"请求失败"}', content_type='application/json')

class RealAuthView(View):
    def post(self, request):
        form = RealAuthForm(request.POST)
        if form.is_valid():
            real_auth_record = RealAuth.objects.filter(applier=request.user.username)
            # //记录存在则插入到已存在表单
            if real_auth_record.exists():
                form = RealAuthForm(request.POST, request.FILES, instance=real_auth_record.first())
                form.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse('{"status":"请求失败"}', content_type='application/json')





