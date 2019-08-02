from django.shortcuts import render
from django.http import Http404
from .models import Blog, BlogType


def blog_list(request):
    context = {}
    context['blogs'] = Blog.objects.all()
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
    context = {}
    try:
        blog_type = BlogType.objects.get(pk=blog_type_pk)
    except BlogType.DoesNotExist:
        raise(Http404(), 'blog_type not exist!')
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    return render(request, 'blog_with_type.html', context=context)
