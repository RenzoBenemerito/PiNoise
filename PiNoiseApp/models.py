from django.db import models

class Users(models.Model):
    fName = models.CharField(max_length=45)
    mName = models.CharField(max_length=45)
    lName = models.CharField(max_length=45)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=45)
    pic = models.ImageField(upload_to='profile_pic',blank=True)
    governmentEntity = models.IntegerField(blank=True,default=0)

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
    
    def Post_title(self):
        return self.title

    def Post_author(self):
        return self.author

    def Post_category(self):
        return self.category

class Votes(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    vote = models.CharField(max_length=45)

    def __int__(self):
        return self.user.id

class ReplyPost(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    author = models.ForeignKey(Users,on_delete=models.CASCADE)
    reply = models.CharField(max_length=1000)
    date_posted = models.DateField(auto_now=True)

class ReplytoReply(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    replyToPost = models.ForeignKey(ReplyPost,on_delete=models.CASCADE)
    replyToComment = models.CharField(max_length=1000)
    author = models.ForeignKey(Users,on_delete=models.CASCADE)
    date_posted = models.DateField(auto_now=True)

class Reports(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    offence = models.CharField(max_length = 45)

    def title(self):
        return self.post.title

    def author(self):
        return self.post.author

    def reporter(self):
        fName = self.user.fName +" "+ self.user.mName +" "+ self.user.lName
        return fName 

    def reason(self):
        return self.offence