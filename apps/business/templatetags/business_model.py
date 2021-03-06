from django import template
from django.utils.safestring import mark_safe
from utils.bitStatesUtils import BitStatesUtils
from certification.models import RealAuth, UserFile,BaseAudit
from business.models import PlatformBankInfo,UserBanknInfo
from django.db.models import Q, Sum

from business.models import BidRequest,AccountFlow
from utils.BidConst import BidConst
from utils.DecimalFormatUtil import DecimalFormatUtil
from django.db.models import Q
register = template.Library()


@register.simple_tag()
def all_bid_request_objs():
    query = BidRequest.objects.filter(bidRequestState=BidConst.GET_BIDREQUEST_STATE_BIDDING())
    return query


@register.simple_tag()
def formate_decimal_show(value):
    return DecimalFormatUtil.formatBigDecimal(value, BidConst.DISPLAY_SCALE())


@register.simple_tag()
def is_bidding(bidRequest):
    if bidRequest.bidRequestState == BidConst.GET_BIDREQUEST_STATE_BIDDING():
        return True
    return False


@register.simple_tag()
def all_bank_type():
    return PlatformBankInfo.BANK_NAME_CCHOICE


@register.simple_tag()
def get_user_bank_info(userProfile):
    return UserBanknInfo.objects.get(userProfile=userProfile)


@register.simple_tag()
def get_bank_type(index):
    all_bank_type_dict = dict(PlatformBankInfo.BANK_NAME_CCHOICE)
    return all_bank_type_dict[int(index)]


@register.simple_tag()
def get_user_file_type(index):
    all_user_file_dict = dict(UserFile.CHOICES)
    return all_user_file_dict[int(index)]


@register.simple_tag()
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.simple_tag()
def get_allAvailableAmountOfinverstorToBidRequest(bidRequest,user):


    bids_temp_query = bidRequest.bids.filter(bidUser=user.get_investor())

    #汇总金额
    available_amount_total =  bids_temp_query.aggregate(Sum('availableAmount'))
    return available_amount_total['availableAmount__sum']



@register.simple_tag()
def get_account_flow_type(index):
    all_account_flow_type_dict = dict(AccountFlow.ACCOUNT_TYPE)
    return all_account_flow_type_dict[int(index)]


@register.simple_tag()
def return_bid_request_history(borrower):
    return  BidRequest.objects.filter((Q(bidRequestState=BidConst.GET_BIDREQUEST_STATE_UNDO())|
                                      Q(bidRequestState=BidConst.GET_BIDREQUEST_STATE_BIDDING_OVERDUE())|
                                      Q(bidRequestState=BidConst.GET_BIDREQUEST_STATE_REJECTED())|
                                      Q(bidRequestState=BidConst.GET_BIDREQUEST_STATE_COMPLETE_PAY_BACK())) &
                                         Q(createUser=borrower))
