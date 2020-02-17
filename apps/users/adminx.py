import xadmin

from .models import EmailVerifyRecord, Banner, Borrower, Investor, UserProfile, BorrowerUserProfile, ManagerProfile, \
    EmploymentDetail, UsersFamilyAuthentication
from xadmin import views
from django.db.models import Q

from django.utils.safestring import mark_safe

class UsersFamilyAuthenticationInline(object):
    model = UsersFamilyAuthentication
    extra = 0

class InvestorInlines(object):
    model = Investor
    extra = 0
    # can_delete = False
    # verbose_name_plural = 'Investor'
    # fk_name = 'userProfile'


class BorrowerInlines(object):
    model = Borrower
    extra = 0
    # can_delete = False
    # verbose_name_plural = 'Borrower'
    # fk_name = 'userProfile'


class UserProfileAdmin(object):
    inlines = [InvestorInlines, UsersFamilyAuthenticationInline]
    list_display = ['username', 'nickname', 'trueName', 'email', 'is_active', 'is_superuser']


    list_filter = ['is_borrower']

    def queryset(self):
        qs = super(UserProfileAdmin, self).queryset()
        qs = qs.filter(is_investor=True)
        return qs

    def nickname(self, obj):
        return obj.profile.nickname  # 自定义字段显示信息

    # nickname.short_description = '昵称'


class BorrowerUserProfileAdmin(object):
    inlines = [BorrowerInlines, UsersFamilyAuthenticationInline]
    list_display = ['username', 'nickname', 'trueName', 'email', 'is_active', ]

    # 可快速编辑
    list_editable = ['username', 'nickname', 'trueName', 'email', 'is_active', ]

    # 只读
    readonly_fields = ['email']
    show_detail_fileds = ['username', 'nickname', 'trueName', 'email', 'is_active', ]
    list_filter = ['is_borrower']

    def queryset(self):
        qs = super(BorrowerUserProfileAdmin, self).queryset()
        qs = qs.filter(is_borrower=True)
        return qs

    def nickname(self, obj):
        return obj.profile.nickname  # 自定义字段显示信息


class ManagerProfileAdmin(object):
    list_display = ['username', 'is_superuser']
    # 只读
    readonly_fields = ['image']
    def queryset(self):
        qs = super(ManagerProfileAdmin, self).queryset()
        qs = qs.filter(is_staff=True)
        return qs


class EmploymentDetailAdmin(object):
    list_display = ['borrower', 'employment_state', 'receive_wage', 'company_type', 'working_life']
    list_filter = ['borrower', 'employment_state']


class EmailVerifyRecordAdmin(object):
    #邮箱显示列
    list_display = ['code', 'email', 'send_type', 'send_time']
    #搜索功能
    search_fields = ['code', 'email', 'send_type']
    #筛选功能
    list_filter = ['code', 'email', 'send_type', 'send_time']
    # pass
    model_icon = 'fa fa-envelope'



class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields =['title', 'image', 'url', 'index']
    list_filter =['title', 'image', 'url', 'index','add_time']


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "P2P网贷后台管理系统"
    site_footer = "P2P小额网贷网"
    menu_style = "accordion"


# xadmin.site.register(Borrower, BorrowerAdmin)
xadmin.site.unregister(UserProfile)
xadmin.site.register(ManagerProfile, ManagerProfileAdmin)
xadmin.site.register(BorrowerUserProfile, BorrowerUserProfileAdmin)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(EmploymentDetail, EmploymentDetailAdmin)
