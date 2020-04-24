import xadmin
from django.db.models import Q
from django.utils import timezone
from .models import RealAuth, RealAuthAuditted, VedioAuth, UserFile, UserFileAudit
from users.models import UserProfile
from utils.bitStatesUtils import BitStatesUtils

class  RealAuthAdmin(object):
    # inlines = [BorrowerInlines, UsersFamilyAuthenticationInline]
    list_display = ['applyTime','idNumber', 'gender', 'remark', 'state',]

    list_filter = ['applyTime','gender']

    # 可快速编辑 #快速编辑不会调用save_models方法
    list_editable = ['auditor', 'state', 'remark']
    exclude = ['file', 'audiTime','auditor','applier',]
    # 只读
    readonly_fields = [ 'applyTime', 'realName', 'gender', 'idNumber', 'bornDate', 'address', 'image1', 'image2']
    ordering = ['state']

    #数据分类
    def queryset(self):
        qs = super(RealAuthAdmin, self).queryset()
        qs = qs.filter(Q(state=BitStatesUtils.STATE_NORMAL())|Q(state=BitStatesUtils.STATE_REJECT()))
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

            user_profile = UserProfile.objects.filter(username=real_auth.applier).first()
            #审核成功给用户添加审核成功状态位
            if real_auth.state == BitStatesUtils.STATE_AUDIT():
                # user_profile = UserProfile.objects.filter(username=real_auth.applier).first()
                user_profile.real_auth_id = real_auth.id
                # 添加审核通过状态位
                user_profile.bitState = BitStatesUtils.addState(user_profile.bitState, BitStatesUtils.GET_OP_REAL_AUTH())
                user_profile.save()

            else:
                # user_profile = UserProfile.objects.filter(username=real_auth.applier).first()
                #用户的实名认证取消
                user_profile.real_auth_id = None
                #状态位更改
                if BitStatesUtils.hasState(user_profile.bitState,BitStatesUtils.GET_OP_REAL_AUTH()):
                    user_profile.bitState= BitStatesUtils.removeState(user_profile.bitState, BitStatesUtils.GET_OP_REAL_AUTH())

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
        qs = qs.filter(state=BitStatesUtils.STATE_AUDIT())
        return qs


class VedioAuthAdmin(object):
    list_display = ['audiTime','applier', 'remark', 'state']
    readonly_fields = ['auditor','audiTime']

    # //审核表，添加审核人
    def save_models(self):
        #获取保持对象
        obj = self.new_obj
        obj.save()
        if obj is not None:
            vedio_auth = obj
            vedio_auth.auditor = self.user.username
            vedio_auth.audiTime = timezone.now()
            #添加视频认证状态位
            user_profile = UserProfile.objects.filter(username=vedio_auth.applier).first()
            user_profile.bitState = BitStatesUtils.addState(user_profile.bitState, BitStatesUtils.GET_OP_VEDIO_AUTH())
            user_profile.save()


class UserFileAdmin(object):
    list_display = ['applyTime', 'applier', 'fileType', 'remark','score', 'state',]
    readonly_fields = ['applier', 'applyTime', 'fileType']
    exclude = ['audiTime','auditor']
    ordering = ['applier', 'fileType']
    list_filter =['applyTime']
    #未审核或者审核失败
    def queryset(self):
        qs = super(UserFileAdmin, self).queryset()
        qs = qs.filter(Q(state=BitStatesUtils.STATE_NORMAL())|Q(state=BitStatesUtils.STATE_REJECT()))
        return qs

    # //审核表，添加审核人
    def save_models(self):
        #获取保持对象
        obj = self.new_obj
        obj.save()
        if obj is not None:
            user_file = obj
            user_file.auditor = self.user.username
            user_file.audiTime = timezone.now()
            user_file.save()
            user_profile_obj = user_file.applier
            #如果审核成功
            if user_file.state == BitStatesUtils.STATE_AUDIT():
                user_profile_obj.score = user_profile_obj.score + user_file.score
                user_profile_obj.save()



class UserFileAudittedAdmin(object):
    list_display = ['state', 'applier', 'applyTime', 'audiTime', 'auditor', 'remark', 'score']
    readonly_fields = ['state', 'applier', 'applyTime', 'audiTime', 'auditor', 'remark', 'score']
    ordering = ['applier','fileType']
    list_filter =['applyTime']
    def queryset(self):
        qs = super(UserFileAudittedAdmin, self).queryset()
        qs = qs.filter(state=BitStatesUtils.STATE_AUDIT())
        return qs





xadmin.site.register(RealAuth, RealAuthAdmin)
xadmin.site.register(RealAuthAuditted,RealAuthAudittedAdmin)
xadmin.site.register(VedioAuth, VedioAuthAdmin)
xadmin.site.register(UserFile, UserFileAdmin)
xadmin.site.register(UserFileAudit, UserFileAudittedAdmin)