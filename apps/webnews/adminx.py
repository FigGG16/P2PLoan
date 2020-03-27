from .models import News, Banner
import xadmin
class NewsAdmin(object):
    list_display = ['name', 'detail', 'publishTime']
    search_fields =['name', 'detail', 'publishTime']
    style_fields = {"detail":"ueditor"}

class BannerAdmin(object):
    list_display = ['title', 'image', 'add_time']
    search_fields =['title', 'image',  'add_time']


xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(News, NewsAdmin)

