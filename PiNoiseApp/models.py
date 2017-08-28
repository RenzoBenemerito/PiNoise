from django.db import models

class Users(models.Model):
    fName = models.CharField(max_length=45)
    mName = models.CharField(max_length=45)
    lName = models.CharField(max_length=45)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=45)
    
    def __int__(self):
        return self.id

class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Posts(models.Model):
    author_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    author = models.CharField(max_length=45)
    title = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    date_posted = models.DateField(auto_now=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    
class Votes(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    vote = models.CharField(max_length=45)

    def __int__(self):
        return self.user.id

class ReplyPost(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    author = models.CharField(max_length=45)
    reply = models.CharField(max_length=1000)
    
