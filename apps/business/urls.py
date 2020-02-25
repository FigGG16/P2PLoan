from django.conf.urls import url

from .views import BidRequest, BorrowTypeList
from django.views.generic import TemplateView

app_name = 'business'



urlpatterns = [


    # return data
    url(r'^borrow_type_list/$', BorrowTypeList.as_view(), name="borrow_type_list"),

    url(r'^check_in_bid/$', BidRequest.as_view(), name="check_in_bid"),

    url(r'^exist_bid/$', TemplateView.as_view(template_name=""), name="exist_bid"),
    # url(r'^real_auth_save/$', RealAuthView.as_view(), name="real_auth_info"),
    #风控材料上传文件执行


]