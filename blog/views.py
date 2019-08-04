from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Blog, BlogType


def blog_list(request):
    page_num = request.GET.get('page', 1) # 获取页码参数，get请求
    blogs_list = Blog.objects.all()
    paginator = Paginator(blogs_list, settings.BLOG_NUM_EACH_PAGE) # 每5篇进行分页
    page_content = paginator.get_page(page_num)
    page_current = page_content.number # 获取当前页码
    page_range = [i for i in range(page_current-2, page_current+3)
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

    context = {}
    context['blogs'] = page_content.object_list
    context['page_content'] = page_content
    context['page_range'] = page_range
    context['blog_count'] = Blog.objects.all().count()
    context['blog_types'] = BlogType.objects.all()
    return render(request, "blog_list.html", context=context)


def blog_detail(request, blog_pk):
    try:
        blog = Blog.objects.get(pk=blog_pk)
        context = dict(blog=blog)
        return render(request, "blog_detail.html", context=context)
    except Blog.DoesNotExist:
        raise(Http404, 'blog id {0} not exist!'.format(blog_pk))


def blogs_with_type(request, blog_type_pk):
    try:
        blog_type = BlogType.objects.get(pk=blog_type_pk)
    except BlogType.DoesNotExist:
        raise(Http404(), 'blog_type not exist!')
    page_num = request.GET.get('page', 1)  # 获取页码参数，get请求
    blogs_list = Blog.objects.filter(blog_type=blog_type)
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

    context = {}
    context['blogs'] = page_content.object_list
    context['blog_type'] = blog_type
    context['page_content'] = page_content
    context['page_range'] = page_range
    context['blog_count'] = Blog.objects.all().count()
    context['blog_types'] = BlogType.objects.all()

    return render(request, 'blog_with_type.html', context=context)
