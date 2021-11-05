from django.db import models
from categorys.models import categorys

# Create your models here.
class Blogs(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    content = models.TextField()
    category = models.ForeignKey(categorys,on_delete = models.CASCADE)
    writer = models.CharField(max_length = 255)
    image = models.ImageField(upload_to = "blogImages",blank = True)
    created = models.DateTimeField(auto_now_add = True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name
