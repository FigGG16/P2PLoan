import xadmin

from .models import EmailVerifyRecord,  Borrower, Investor, UserProfile, BorrowerUserProfile, ManagerProfile, \
    EmploymentDetail,  Account
from xadmin import views
from django.db.models import Q

from django.utils.safestring import mark_safe



class AccountInline(object):
    model = Account
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

#投资者
class UserProfileAdmin(object):
    search_fields = ['username']
    inlines = [InvestorInlines, AccountInline]
    list_display = ['username', 'nickname', 'trueName', 'email', 'is_active', 'is_superuser']
    readonly_fields = ['email', 'image']

    list_filter = ['is_borrower']
    def queryset(self):
        qs = super(UserProfileAdmin, self).queryset()
        qs = qs.filter(is_investor=True)
        return qs

    def nickname(self, obj):
        return obj.profile.nickname  # 自定义字段显示信息

    # nickname.short_description = '昵称'


class BorrowerUserProfileAdmin(object):
    inlines = [BorrowerInlines, AccountInline]
    list_display = ['username', 'nickname', 'trueName', 'email', 'is_active', ]
    search_fields =['username']
    autocomplete_fields =['username']

    # 可快速编辑
    list_editable = ['username', 'nickname', 'trueName', 'email', 'is_active', ]

    # 只读
    readonly_fields = ['email', 'image']
    show_detail_fileds = ['username', 'nickname', 'trueName', 'email', 'is_active', ]
    list_filter = ['is_borrower','username']

    autocomplete_fields = ('circassian_word',)



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
    # autocomplete_fields = ['borrower']
    search_fields = ['borrower']
    list_display = ['borrower', 'employment_state', 'receive_wage', 'company_type', 'working_life']
    list_filter = ['borrower', 'employment_state']
    def save_models(self):
        #获取保持对象
        obj = self.new_obj
        obj.save()


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

    def get_site_menu(self):  #名称不能改
        return [
            {
                'title': '数据统计',
                'icon': 'fa fa-bar-chart-o',
                'menus': (
                    {
                        'title': '首页',    #这里是你菜单的名称
                        'url': '/xadmin/chart',     #这里填写你将要跳转url
                        'icon': 'fa fa-cny'     #这里是bootstrap的icon类名，要换icon只要登录bootstrap官网找到icon的对应类名换上即可
                    },

                )
            }
        ]

from .views import Chart
xadmin.site.register_view(r'^chart/$', Chart, name='chart')
# url(r'^chart/$', Chart.as_view(), name='chart'),

# xadmin.site.register(Borrower, BorrowerAdmin)
xadmin.site.unregister(UserProfile)
xadmin.site.register(ManagerProfile, ManagerProfileAdmin)
xadmin.site.register(BorrowerUserProfile, BorrowerUserProfileAdmin)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(EmploymentDetail, EmploymentDetailAdmin)
