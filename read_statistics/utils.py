import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from .models import ReadNum, ReadDetail


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        # 总阅读数+1
        readNumObj, _ = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readNumObj.read_num += 1
        readNumObj.save()

        # 每天阅读数+1
        date = timezone.now().date()
        if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():
            readDetailObj = ReadDetail.objects.get(content_type=ct, object_id=obj.pk, date=date)
        else:
            readDetailObj = ReadDetail(content_type=ct, object_id=obj.pk, date=date)

        readDetailObj.read_num += 1
        readDetailObj.save()

    return key


def get_seven_days_read_num(content_type):
    today = timezone.now().date()

    read_nums = []
    dates = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)

    return dates, read_nums


def get_today_hot_data(content_type):
    pass