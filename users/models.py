from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Customuser(AbstractUser):                                                 # abstracting the django's Default User model
    image = models.ImageField(upload_to='images', default ='images/images.png') # image field with a default image


class Blog(models.Model):                                                       # Blog model
    title = models.CharField(max_length=100)                                    # fields include title,content, user
    content = models.TextField()
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):                                                     # Comment model
    content = models.TextField()                                                 # fields include content, user, blog 
    user    = models.ForeignKey(Customuser, on_delete=models.CASCADE)
    blog    = models.ForeignKey(Blog, on_delete=models.CASCADE , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)