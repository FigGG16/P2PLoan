from PIL import Image
from django import forms
from django.core.files import File
from .models import RealAuth, UserFile
from django.db.models import Q
# 保存图片1
class ReturnRealAuthImageForm(forms.ModelForm):

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())


    class Meta:
        model = RealAuth
        fields = ('file', 'x', 'y', 'width', 'height',)
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': 'image/*' # this is not an actual validation! don't rely on that!
            })
        }

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', '')
    #     super(ReturnRealAuthImageForm, self).__init__(*args, **kwargs)




    def save(self, user):
            realauth = super(ReturnRealAuthImageForm, self).save(commit=False)
            #存储申请人
            # 判断存储哪一张认证图片

            #image1上传
            if self.data.get("image1", "") == 'True':
                realauth.image1 = realauth.file
             #image2上传
            elif self.data.get("image2", "") == 'True':
                realauth.image2 = realauth.file
            # //保存申请人
            realauth.applier = user
            # realauth.applier = self.data.get("applier", "")
            realauth.save()

            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')

            #根据判断返回图片
            if self.data.get("image1", "") == 'True':
                image = Image.open(realauth.image1)
            else:
                image = Image.open(realauth.image2)
            cropped_image = image.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)

            #根据判断返回图片
            if self.data.get("image1", "") == 'True':
                resized_image.save(realauth.image1.path)
            else:
                resized_image.save(realauth.image2.path)
            return realauth

class RealAuthForm(forms.ModelForm):
    class Meta:
        model = RealAuth
        fields = ('realName','gender','idNumber','bornDate','address')

    def save(self):
        realauth = super(RealAuthForm, self).save()
        return  realauth

#用户上传风控材料执行
class UserFileForm(forms.ModelForm):

    class Meta:
        model = UserFile
        fields = ('image',)

    def save(self, user):
        user_file = super(UserFileForm, self).save(commit=False)
        user_file.applier = user
        user_file.save()
        return user_file

class UserFileTypeForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ()

    def save(self, user):
        user_file = super(UserFileTypeForm, self).save()
        user_file_query = UserFile.objects.filter(Q(applier=user)&Q(fileType=0)) #0==无 表示为分类

        #给每张图片分类
        if user_file_query.exists():
            fileTypeList = self.data.getlist("fileType", "")
            for imageType, user_file_obj in zip(fileTypeList,user_file_query):
                user_file_obj.fileType = int(imageType)
                user_file_obj.save()

        return user_file