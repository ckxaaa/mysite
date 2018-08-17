from django.shortcuts import get_object_or_404,render
from .models import Blog,BlogType,ReadNum
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
# from datetime import datetime
# Create your views here.


def get_blog_list_common_data(request,blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOG_NUMBER)  # 每10页进行扉页
    page_num = request.GET.get('page', 1)  # 获取页码参数
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number  # 获取当前页码
    # 获取当前页码前后各两位
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #获取日期分类对应得博客数量

    blog_dates = Blog.objects.dates('created_time','month',order='DESC')
    blog_dates_dict = {}
    for blog_date in  blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count



    # 获取博客分类得对应博客数量

    '''
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
    '''
    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blog'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request,blogs_all_list)
    #context['blogs_count'] = Blog.objects.all().count
    return render(request,'blog_list.html',context)

def blogs_with_type(request,blog_type_pk):

    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request,blogs_all_list)
    context['blog_type'] = blog_type
    return render(request,'blogs_with_type.html',context)

def blog_with_date(request,year,month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_blog_list_common_data(request,blogs_all_list)
    context['blog_with_date'] = '%s年%s月' %(year,month)
    return render(request,'blogs_with_date.html', context)


def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    if not request.COOKIES.get('blog_%s_read' % blog_pk):
        if ReadNum.objects.filter(blog=blog).count():
            #存在记录
            readnum = ReadNum.objects.get(blog=blog)
        else:
            #不存在记录
            readnum = ReadNum(blog=blog)
        #计数加一
        readnum.read_num += 1
        readnum.save()
    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog

    response =  render(request,'blog_detail.html',context) #响应
    response.set_cookie('blog_%s_read' % blog_pk,'true') #也可以使用expires=datetime 阅读cookie标记
    return response

