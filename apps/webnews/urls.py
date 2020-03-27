from django.conf.urls import url, include

from .views import NewsView,NewDetail

app_name = 'webnews'

urlpatterns = [

    url('^$', NewsView.as_view(), name="news"),
    url('^new_detail$', NewDetail.as_view(), name="news_detail"),

]