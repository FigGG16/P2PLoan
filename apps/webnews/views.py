from django.shortcuts import render
from .models import Banner,News
from django.views.generic.base import View
from django.views.generic.list import ListView
# Create your views here.


class NewsView(ListView):
    # def get_queryset(self):
    #     filter_val = self.request.GET.get('filter', None)
    #     if filter_val == None or filter_val == '0':
    #         return self.queryset
    #     new_context =BidRequest.objects.filter(bidRequestState=int(filter_val))
    #
    #     return new_context
    model = News
    template_name = 'news.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'news'  # Default: object_list
    paginate_by = 10
    queryset = News.objects.all().order_by("-publishTime")


class NewDetail(View):
    def get(self,request):
        nid = request.GET.get('nid')
        new = News.objects.get(id=nid)
        return render(request,'new_detail.html',{'new':new})