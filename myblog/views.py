from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_num, get_today_hot_data
from blog.models import Blog


def home(request):
    ct = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_num(ct)
    today_hot_data = get_today_hot_data(ct)

    context = dict()
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['hot_data'] = today_hot_data
    return render(request, 'home.html', context=context)
