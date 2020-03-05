from django import template
from django.utils.safestring import mark_safe
from utils.bitStatesUtils import BitStatesUtils
from certification.models import RealAuth, UserFile,BaseAudit
from business.models import BidRequest
from django.db.models import Q
from users.models import Account
register = template.Library()

#user是否存在实名认证记录
@register.simple_tag()
def is_real_audited(user_profile):
    real_auth_query = RealAuth.objects.filter(applier=user_profile)
    if real_auth_query.exists():
        return True
    return False


#是否未审核？
@register.simple_tag()
def is_real_audit_normal(user_profile):
    if not (user_profile.bitState is None):
        if BitStatesUtils.hasState(user_profile.bitState, BitStatesUtils.GET_OP_REAL_AUTH()):
            return True
    return False


@register.simple_tag()
def all_user_file_type():
    return UserFile.CHOICES

#判断是否存在
@register.simple_tag()
def is_exist_none_file_type_field(userFileSet):
    for obj in userFileSet:
        if obj.fileType == 0:
            return True
    return False

@register.simple_tag()
def get_user_file_type(index):
    usr_file_choice_dict = dict(UserFile.CHOICES)
    print(usr_file_choice_dict[index])
    return usr_file_choice_dict[index]


#文件是否审核
@register.simple_tag()
def get_user_file_state(index):
    return dict(BaseAudit.CURRENT_STATE_CHOICE)[index]


@register.simple_tag()
def is_biding(user_profile):
    query_bid_requst = BidRequest.objects.filter(createUser=user_profile)
    if query_bid_requst.exists():
        return True
    return False

#获取用户账户
@register.simple_tag()
def get_user_account(user):
    user_account_obj = Account.objects.get(userProfile=user)
    return user_account_obj
# @register.simple_tag(name
# ='get_user_id')
# def get_user_identity_number(user_profile):
#     user_profile_detail = user_profile.Person.objects.get(name='alex')
#     if user_profile.real_auth_id is None:
#         return False
#     elif BitStatesUtils.hasState(user_profile.bitState, BitStatesUtils.GET_OP_REAL_AUTH()):
#         return True
#
#     return False