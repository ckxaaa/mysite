from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import exceptions
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

# Create your models here.


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)
    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=30)
    blog_type = models.ForeignKey(BlogType,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk':self.pk})

    def get_email(self):
        return self.author.email


    def __str__(self):
        return '<Blog:%s>' % self.title

    class Meta:
        ordering = ["-created_time"]

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog,on_delete=models.CASCADE)




