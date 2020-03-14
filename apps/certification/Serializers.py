from rest_framework import serializers
from .models import RealAuth, UserFile
from django.contrib.auth import get_user_model
from P2PLoan.settings import REGEX_MOBILE
from datetime import datetime
from datetime import timedelta
from .models import VerifyCode
import re
User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """


        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class RealAuthSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default = 'success', read_only=True)
    image1 = serializers.SerializerMethodField()
    image2 = serializers.SerializerMethodField()

    class Meta:
        model = RealAuth
        fields = ('status','image1', 'image2')

        # if photo and hasattr(photo, 'url'):
        #     photo_url = car.photo.url
        #     return request.build_absolute_uri(photo_url)
        # else:
        #     return None

    #获取图片的绝对url
    def get_image1(self, realauth):
        request = self.context.get('request')
        if realauth.image1 and hasattr(realauth.image1, 'url'):
            image1 = realauth.image1.url
            return request.build_absolute_uri(image1)
        else:
            return "False"

    def get_image2(self, realauth):
        request = self.context.get('request')
        if realauth.image2 and hasattr(realauth.image2, 'url'):
            image2 = realauth.image2.url
            return request.build_absolute_uri(image2)
        else:
            return "False"

    #规避图片出错
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['image1']:
            data['image1'] = "False"
        if not data['image2']:
            data['image2'] = "False"
        return data


class UserFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = ('image')

    def get_image1(self, userfile):
        request = self.context.get('request')
        if userfile.image1 and hasattr(userfile.image1, 'url'):
            image = userfile.image.url
            return request.build_absolute_uri(image)






