from django.conf.urls import url, include

from .views import RealAuthImageView, RealAuthView

app_name = 'certification'

urlpatterns = [


    # return data
    url(r'^return_auth_image/$', RealAuthImageView.as_view(), name="return_image"),
    url(r'^real_auth_save/$', RealAuthView.as_view(), name="real_auth_info"),
    # # 用户家庭信息保存
    # url(r'^family_info_Save/$', UserFamilyProfileView.as_view(), name="user_family_info"),
    #
    # # 用户单位信息保存
    # url(r'^company_info_Save/$', UserCompanyProfileView.as_view(), name="user_company_info"),
    #
    # # 用户头像上传
    # url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    #
    # # 用户验证资料上传
    # url(r'^authentication/$', UploadUserAuthenticationView.as_view(), name="authentication_upload"),
    # # url(r'^authentication/$', PictureCreateView.as_view(), name="authentication_upload"),
    #
    # # 用户材料删除
    # # url('delete/<int:pk>', UploadUserAuthenticationDeleteView.as_view(), name='upload-delete'),
    #
    # path('delete/<int:pk>', UploadUserAuthenticationDeleteView.as_view(), name='upload-delete'),
    #
    # #用户验证材料显示
    # url('view/', UploadUserAuthenticationListView.as_view(), name='upload-view'),

    # 用户验证资料上传
    # url(r'^authentication/$', PictureCreateView.as_view(), name="upload-new"),

    # url(r'^view/$', PictureListView.as_view(), name='upload-view'),
]