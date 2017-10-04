from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User
class Users(models.Model):
    user = models.OneToOneField(User)

    pic = models.ImageField(upload_to='profile_pic',blank=True)
    governmentEntity = models.IntegerField(blank=True,default=0)

    def get_user(self):
        return self.user

    def get_email(self):
        return self.user.first_name

class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Posts(models.Model):
    author_id = models.ForeignKey(User,on_delete=models.CASCADE)
    author = models.CharField(max_length=45)
    title = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    date_posted = models.DateField(auto_now=True)
    pic = models.ImageField(upload_to='post_pic',blank=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    
    def Post_title(self):
        return self.title

    def Post_author(self):
        return self.author

    def Post_category(self):
        return self.category

class Votes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    vote = models.CharField(max_length=45)

    def __int__(self):
        return self.user.id

class ReplyPost(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    reply = models.CharField(max_length=1000)
    date_posted = models.DateField(auto_now=True)

class ReplytoReply(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    replyToPost = models.ForeignKey(ReplyPost,on_delete=models.CASCADE)
    replyToComment = models.CharField(max_length=1000)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date_posted = models.DateField(auto_now=True)

class Reports(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    offence = models.CharField(max_length = 45)

    def title(self):
        return self.post.title

    def author(self):
        return self.post.author

    def reporter(self):
        username = self.user.username
        return username 

    def reason(self):
        return self.offence