from django import template
from django.utils.safestring import mark_safe
from utils.bitStatesUtils import BitStatesUtils
# from certification.models import RealAuth, UserFile,BaseAudit
from business.models import PlatformBankInfo


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