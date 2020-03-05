from django.conf.urls import url

from .views import BidRequestView, BorrowTypeList, ApplyView, BorrowInfoView, RechargeView,BidView
from django.views.generic import TemplateView

app_name = 'business'



urlpatterns = [


    # return data
    url(r'^borrow_type_list/$', BorrowTypeList.as_view(), name="borrow_type_list"),

    url(r'^check_in_bid/$', BidRequestView.as_view(), name="check_in_bid"),

    url(r'^exist_bid/$', TemplateView.as_view(template_name=""), name="exist_bid"),

    url(r'^bid_apply/$', ApplyView.as_view(), name="bid_apply"),

    url(r'^borrow_info/$', BorrowInfoView.as_view(), name="borrow_info"),

    url(r'^recharge/$', RechargeView.as_view(), name="recharge"),

    url(r'^bid/$', BidView.as_view(), name="bid"),
    # url(r'^real_auth_save/$', RealAuthView.as_view(), name="real_auth_info"),
    #风控材料上传文件执行


]