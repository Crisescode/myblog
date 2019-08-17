from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.conf import settings
from read_statistics.models import ReadNum
from .models import Blog, BlogType


def common_params(request, blogs_list):
    page_num = request.GET.get('page', 1)  # 获取页码参数，get请求
    paginator = Paginator(blogs_list, settings.BLOG_NUM_EACH_PAGE)  # 每5篇进行分页
    page_content = paginator.get_page(page_num)
    page_current = page_content.number  # 获取当前页码
    page_range = [i for i in range(page_current - 2, page_current + 3)
                  if 0 < i <= paginator.num_pages]
    # 中间插入省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类的对应博客数量
    '''
    blog_types = BlogType.objects.all()
    blog_type_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        print("blog_type", blog_type.blog_count)
        blog_type_list.append(blog_type)
    '''
    # 获取日期分类的对应博客数量
    blog_dates = Blog.objects.dates('create_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,
                                         create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_content.object_list
    context['page_content'] = page_content
    context['page_range'] = page_range
    context['blog_count'] = Blog.objects.all().count()
    # context['blog_types'] = blog_type_list
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict

    return context


def blog_list(request):
    blogs_list = Blog.objects.all()
    context = common_params(request, blogs_list)

    return render(request, "blog_list.html", context=context)


def blogs_with_type(request, blog_type_pk):
    try:
        blog_type = BlogType.objects.get(pk=blog_type_pk)
    except BlogType.DoesNotExist:
        raise(Http404(), 'blog_type not exist!')
    blogs_list = Blog.objects.filter(blog_type=blog_type)
    context = common_params(request, blogs_list)
    context['blog_type'] = blog_type

    return render(request, 'blog_with_type.html', context=context)


def blogs_classification_with_date(request, year, month):
    blogs_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
    context = common_params(request, blogs_list)
    context['blog_date'] = '%s年%s月' % (year, month)

    return render(request, 'blog_with_date.html', context=context)


def blog_detail(request, blog_pk):
    try:
        context = {}
        blog = Blog.objects.get(pk=blog_pk)
        if not request.COOKIES.get('blog_%s_readed' % blog_pk):
            ct = ContentType.objects.get_for_model(Blog)

            if ReadNum.objects.filter(content_type=ct, object_id=blog.pk).count():
                readn = ReadNum.objects.get(content_type=ct, object_id=blog.pk)
            else:
                readn = ReadNum(content_type=ct, object_id=blog.pk)

            readn.read_num += 1
            readn.save()

        current_blog_create_time = blog.create_time
        context['blog'] = blog
        context['previous_blog'] = Blog.objects.\
            filter(create_time__gt=current_blog_create_time).last()
        context['next_blog'] = Blog.objects.\
            filter(create_time__lt=current_blog_create_time).first()
        response = render(request, "blog_detail.html", context=context) # 响应
        response.set_cookie('blog_%s_readed' % blog_pk, 'true')

        return response
    except Blog.DoesNotExist:
        raise(Http404, 'blog id {0} not exist!'.format(blog_pk))
