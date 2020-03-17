"""P2PLoan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
import xadmin
from django.conf.urls import url, include
from django.views.static import serve
from django.views.generic import TemplateView #处理静态文件的
from users.views import LoginView, RegisterView, AciveUserView, ForgetPwdView, ResetView, ModifyPwdView, LogoutView, PersonCenterView,  UserAccountView,generic
from P2PLoan.settings import MEDIA_ROOT
from django.urls import include, path
from el_pagination.decorators import page_template, page_templates


from autocomplete import UserProfileAutocomplete

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', TemplateView.as_view(template_name="index.html"), name="index"),
    # url('^login/$', LoginView, name="login"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', AciveUserView.as_view(), name="user_active"),

    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    url(r'^person_centerView/$', PersonCenterView.as_view(), name="person_centerView"),
    url(r'^userAccountView/$',page_templates({'query_history_bid.html':"bids-page",
                                              'query_history_bidRequest.html':"bidRequests-page",
                                              "query_payment_schedule.html":"paymentSchedules-page",})(generic),name="UserAccountView"),



    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 用户信息相关url配置
    url(r'^userAccountView0/', include('users.urls', namespace="users")),

    # 用户资料认证url配置
    url(r'^userAccountView1/', include('certification.urls', namespace="certification")),

    # 用户招标与借标url配置
    url(r'^', include('business.urls', namespace="business")),

    url(r'^category-autocomplete/$', UserProfileAutocomplete.as_view(), name='category-autocomplete'),

]
