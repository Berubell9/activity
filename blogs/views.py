from django.shortcuts import render
from django.http import HttpResponse
from categorys.models import categorys
from .models import Blogs
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here.

def index(request):
    categories = categorys.objects.all()
    blogs = Blogs.objects.all()
    latest = Blogs.objects.all().order_by('-pk')[:2]
    
    #กิจกรรมที่ได้รับรางวัล
    like = Blogs.objects.all().order_by('-views')[:3]

    #pagination
    paginator = Paginator(blogs,4)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        blogPerpage = paginator.page(page)
    except(EmptyPage,InvalidPage):
        blogPerpage = paginator.page(paginator.num_pages)

    return render(request,"frontend/index.html",{'categories':categories,'blogs':blogPerpage,'latest':latest,'like':like})

def blogDetail(request,id):
    like = Blogs.objects.all().order_by('-views')[:3]
    categories = categorys.objects.all()
    singleBlog = Blogs.objects.get(id=id)
    singleBlog.views = singleBlog.views+1
    singleBlog.save()
    return render(request,"frontend/blogDetail.html",{"blog":singleBlog, 'categories':categories, 'like':like})

def searchCategory(request,cat_id):
    categories = categorys.objects.all()
    categoryName = categorys.objects.get(id = cat_id)
    #กิจกรรมที่ได้รับรางวัล
    like = Blogs.objects.all().order_by('-views')[:3]
    blogs = Blogs.objects.filter(category_id = cat_id)
    return render(request,"frontend/searchCategory.html",{"blogs":blogs, 'categories':categories, 'like':like, "categoryName":categoryName})

def searchWriter(request,writer):
    categories = categorys.objects.all()
    like = Blogs.objects.all().order_by('-views')[:3]
    blogs = Blogs.objects.filter(writer = writer)
    return render(request,"frontend/searchWriter.html",{"blogs":blogs, 'categories':categories, 'like':like})
