from django.shortcuts import render, redirect
from blogs.models import Blogs
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from categorys.models import categorys
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

# Create your views here.
@login_required(login_url="member")
def panel(request):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer = writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer = writer).aggregate(Sum("views"))
    return render(request,"backend/index.html",{"blogs":blogs,"writer":writer,"blogCount":blogCount,"total":total})

@login_required(login_url="member")
def displayForm(request):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer = writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer = writer).aggregate(Sum("views"))
    categories = categorys.objects.all()
    return render(request,"backend/blogForm.html",{"blogs":blogs,"writer":writer,"blogCount":blogCount,"total":total, "categories":categories})

@login_required(login_url="member")
def insertData(request):
    try:
        if request.method == "POST" and request.FILES["image"]:
            datafile = request.FILES["image"]
            #รับคำจากฟอร์ม
            name = request.POST["name"]
            category = request.POST["category"]
            description = request.POST["description"]
            content = request.POST["content"]
            writer = auth.get_user(request)

            if str(datafile.content_type).startswith("image"):
                #อัพโหลดรูป
                fs = FileSystemStorage()
                img_url = "blogImages/"+datafile.name
                filename = fs.save(img_url,datafile)
                #บันทึกข้อมูลบทความ
                blog = Blogs(name=name,category_id=category,description=description,content=content,writer=writer,image=img_url)
                blog.save()
                messages.info(request,"อัพโหลดข้อมูลสำเร็จ")
                return redirect("displayForm")
            else:
                messages.info(request,"อัพโหลดไม่สำเร็จ กรุณาอัพโหลดใหม่อีกครั้ง")
                return redirect("displayForm")
    except:
        return redirect("displayForm")

@login_required(login_url="member")
def deleteData(request,id):
    try:
        blog = Blogs.objects.get(id = id)
        fs = FileSystemStorage()
        #ลบภาพปก
        fs.delete(str(blog.image))
        #ลบข้อมูลออกจากฐานข้อมูล
        blog.delete()
        return redirect('panel')
    except:
        return redirect('panel')

@login_required(login_url="member")
def editData(request,id):
    #ข้อมูล
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer = writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer = writer).aggregate(Sum("views"))
    categories = categorys.objects.all()

    blogEdit = Blogs.objects.get(id = id)
    return render(request,"backend/editForm.html",{"blogEdit":blogEdit,"writer":writer,"blogCount":blogCount,"total":total,"categories":categories})
    
@login_required(login_url="member")
def updateData(request,id):
    try:
        if request.method == "POST":
            #ดึงข้อมูลที่เเก้ไขมาใช้งาน
            blog = Blogs.objects.get(id = id)
            #รับคำจากฟอร์ม
            name = request.POST["name"]
            category = request.POST["category"]
            description = request.POST["description"]
            content = request.POST["content"]
            #อัพเดตข้อมูล
            blog.name = name
            blog.category_id = category
            blog.description = description
            blog.content = content
            blog.save()
            #อัพเดตรูป
            if request.FILES["image"]:
                datafile = request.FILES["image"]
                if str(datafile.content_type).startswith("image"):
                    #ลบภาพจริงออก
                    fs =  FileSystemStorage()
                    fs.delete(str(blog.image))
                    #เเทนที่ภาพใหม่
                    img_url = "blogImages/"+datafile.name
                    filename = fs.save(img_url,datafile)
                    blog.image = img_url
                    blog.save()
            return redirect("panel")
    except:
        return redirect("panel")