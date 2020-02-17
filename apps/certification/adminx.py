import xadmin
from django.db.models import Q
from django.utils import timezone
from .models import RealAuth, RealAuthAuditted
from users.models import UserProfile
from utils.bitStatesUtils import BitStatesUtils

class  RealAuthAdmin(object):
    # inlines = [BorrowerInlines, UsersFamilyAuthenticationInline]
    list_display = ['applyTime', 'applier','idNumber', 'gender', 'remark', 'state']

    list_filter = ['applyTime','gender','state']

    # 可快速编辑
    list_editable = ['auditor', 'state', 'remark']
    exclude = ['file', 'audiTime']
    # 只读
    readonly_fields = ['applier', 'applyTime', 'realName', 'gender', 'idNumber', 'bornDate', 'address', 'image1', 'image2']
    ordering = ['state']

    def queryset(self):
        qs = super(RealAuthAdmin, self).queryset()
        qs = qs.filter(Q(state='1')|Q(state='3'))
        return qs

    # //审核表，添加审核人
    def save_models(self):
        #获取保持对象
        obj = self.new_obj
        obj.save()
        if obj is not None:
            real_auth = obj
            real_auth.auditor = self.user.username
            real_auth.audiTime = timezone.now()

            #审核成功给用户添加审核成功状态位
            if real_auth.state == BitStatesUtils.GET_STATE_AUDIT():
                user_profile = UserProfile.objects.filter(username=real_auth.applier).first()
                user_profile.real_auth_id = real_auth.id
                # 添加审核通过状态位
                user_profile.bitState = BitStatesUtils.addState(user_profile.bitState, BitStatesUtils.GET_STATE_AUDIT())

                user_profile.save()

            else:
                user_profile = UserProfile.objects.filter(username=real_auth.applier).first()
                user_profile.real_auth_id = None


                user_profile.save()

            # real_auth.course_nums = Course.objects.filter(course_org=course_org).count()
            real_auth.save()

#审核通过
class RealAuthAudittedAdmin(object):
    list_display = ['applyTime', 'applier', 'idNumber', 'gender','remark', 'audiTime', 'state', 'auditor']
    readonly_fields = ['state', 'applier', 'applyTime', 'realName', 'gender', 'idNumber', 'bornDate', 'address', 'image1', 'image2', 'audiTime', 'auditor','remark']
    exclude = ['file']

    def queryset(self):
        qs = super(RealAuthAudittedAdmin, self).queryset()
        qs = qs.filter(state='2')
        return qs



xadmin.site.register(RealAuth, RealAuthAdmin)
xadmin.site.register(RealAuthAuditted,RealAuthAudittedAdmin)
