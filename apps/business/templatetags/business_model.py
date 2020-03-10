from django import template
from django.utils.safestring import mark_safe
from utils.bitStatesUtils import BitStatesUtils
# from certification.models import RealAuth, UserFile,BaseAudit
from business.models import PlatformBankInfo,UserBanknInfo


from business.models import BidRequest
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


