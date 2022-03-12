from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
from django.core.paginator import Paginator

# Create your views here.
def hello_world(request):
    return HttpResponse("hello world")


def article_content(request):
    article = Article.objects.all()[0]
    title = article.title
    brief_content = article.brief_content
    content = article.content
    article_id = article.article_id
    publish_date = article.publish_date
    return_str = 'title: %s, bref_content: %s, '\
                'content: %s, article_id: %s, publish_date: %s' % (title,
                                                                   brief_content,
                                                                   content,
                                                                   article_id,
                                                                   publish_date

    )
    return HttpResponse(return_str)

def get_index_page(request):
    page = request.GET.get('page')  # 获取url 参数
    if page:
        page = int(page)
    else:
        page = 1
    top5article_list = Article.objects.order_by('-publish_date')[:5]
    all_article = Article.objects.all()
    paginator = Paginator(all_article, 3)
    page_article_list = paginator.page(page)
    page_num = paginator.num_pages
    if page_article_list.has_next():
        next_page = page +1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    return render(request, 'blog/index1.html',
                  {
                      'article_list': page_article_list,
                      'top5article_list': top5article_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous_page': previous_page

                  }
                  )

def get_detail_page(request, article_id):
    all_article = Article.objects.all()
    curr_article = None
    previous_article = None
    next_article = None
    # previous_index = 0
    # next_index = 0

    for index, article in enumerate(all_article):
        # 为什么用index不用article_id我觉得article_id不一定连续
        if index == 0:
            previous_index = len(all_article)-1
            next_index = index + 1
        elif index == len(all_article)-1:
            previous_index = index - 1
            next_index = 0
        else:
            previous_index = index - 1
            next_index = index + 1

        if article.article_id == article_id:
            curr_article = article
            previous_article = all_article[previous_index]
            next_article = all_article[next_index]
            break

    section_list = curr_article.content.split('\n')
    return render(request, 'blog/detail1.html',
                  {
                      'curr_article': curr_article,
                      'section_list': section_list,
                      'previous_article': previous_article,
                      'next_article': next_article
                  }
                  )


# 接收请求数据
def search(request):
    request.encoding='utf-8'
    if 'q' in request.GET and request.GET['q']:
        message = request.GET['q']
        all_article = Article.objects.filter(title__contains=message)
    else:
        all_article = Article.objects.all()

    page = request.GET.get('page')  # 获取url 参数

    if page:
        page = int(page)
    else:
        page = 1
    top5article_list = Article.objects.order_by('-publish_date')[:5]
    paginator = Paginator(all_article, 3)
    page_article_list = paginator.page(page)
    page_num = paginator.num_pages
    if page_article_list.has_next():
        next_page = page +1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    return render(request, 'blog/index1.html',
                  {
                      'article_list': page_article_list,
                      'top5article_list': top5article_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous_page': previous_page

                  }
                  )
# 局部更新实验，加法功能

def partindex(request):
    return render(request, './add.html')

def add(request):
    a = request.GET['a']
    b = request.GET['b']
    if request.is_ajax():
        ajax_string = 'ajax request:'
    else:
        ajax_string = 'not ajax request:'
    c = int(a) + int(b)
    r = HttpResponse(ajax_string + str(c))
    return r
