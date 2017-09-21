from django.shortcuts import render, redirect
from . models import User, Users, Posts, Category, Votes, ReplyPost, ReplytoReply, Reports
from django import forms
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpRequest
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings as conf_settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

def index(request,methods=['POST']):

    if request.method == 'POST':
        fName = request.POST['fName']
        lName = request.POST['lName']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']

        user = User(first_name = fName,last_name = lName,username = username, email = email,password = password)
        user.set_password(user.password)
        user.save()

        userStat = Users(governmentEntity = 0)
        userStat.user = user
        userStat.save()

    return render(request, 'index.html')

@login_required
def dash(request):
    user = request.user
    category = Category.objects.all()
    return render(request,'dashboard.html',{'user':user,'category':category})


def user_login(request,methods=['POST']): 
    if(request.method == 'POST'):
        userLog = request.POST['userLog']
        passLog = request.POST['passLog']
        log = authenticate(username = userLog, password = passLog);
        if log:
            login(request,log)
            return redirect('/pinoise/dashboard')
        else:
            return messages.error(request, 'No Account with such credentials.')
    else:
        return redirect('/pinoise')

@login_required
def user_logout(request):
    logout(request)
    return render(request,'index.html')

@login_required
def problemPage(request,problem):
    posts = Posts.objects.filter(category = problem)
    vote = Votes.objects.filter(user = request.user.id)
    for p in posts:
        for v in vote:
            if p.id == v.post.id:
                if v.vote == "upvote":
                    p.vote = "upvote"
                elif v.vote == "downvote":
                    p.vote = "downvote"

    user = request.user

    return render(request,'Category.html',{'problem':problem,'posts':posts,'votes':vote,'userLog':request.user,'user':user})

def postIdea(request,problem,methods=['POST']):
    if(request.method == 'POST'):
        title = request.POST['title']
        description = request.POST['ideation']
        category = request.POST['category']
        category1 = Category.objects.get(category=category)
        poster = request.user
        username = poster.username
        post = Posts(author_id = poster,author = username,title = title,description = description,category_id = category1,category = category1.category)
        post.save()
    
        return redirect('./')

def updateIdea(request,titleBefore,methods=['POST']):
    if(request.method == 'POST'):
        title = request.POST['title']
        description = request.POST['ideation']
        category = request.POST['category']
        category1 = Category.objects.get(category=category)
        poster = request.user
        post = Posts.objects.get(author_id = poster,title = titleBefore,category_id = category1,category = category1.category)
        post.title = title
        post.description = description
        post.save()
        url = '../'+title +'/post_page'
        return redirect(url)

def idea(request):
    user = request.user
    posts = Posts.objects.filter(author_id=request.user.id)
    return render(request,'myIdeas.html',{'posts':posts,'user':user})

def deletePost(request,methods=['GET']):
    title = request.GET['title']
    posts = Posts.objects.filter(title = title, author_id = request.user.id)
    posts.delete()
    return redirect('./')

def settings(request,methods=['POST']):
    userLog = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, form.user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
        else:
            return redirect('settings')
    else:
        form = PasswordChangeForm(request.user, request.POST)
        return render(request, 'settings.html',{'user':userLog,'form':form})
        
def vote(request,methods=['GET']):
    title = request.GET['title']
    kind = request.GET['kind']
    author = request.GET['author']
    post = Posts.objects.get(title = title,author = author)
    try:
        check = Votes.objects.get(user = request.user.id, post = post.id)
    except Votes.DoesNotExist:
        check = None
    if check is None:
        voter = Votes(user = request.user,post = post,vote = kind)
        voter.save();
        if kind == 'upvote':
            post.like = post.like + 1
        elif kind == 'downvote':
            post.dislike = post.dislike + 1
        post.rating = post.like - post.dislike
        post.save()
    else:
        if  check.vote == kind:
            check.delete() 
            if  kind == 'upvote':
                post.like = post.like - 1
                post.rating = post.like - post.dislike
            elif    kind == 'downvote':
                post.dislike = post.dislike -1
                post.rating = post.like - post.dislike
            post.save()
            
    return redirect('./')

def postPage(request,user,title):
    post = Posts.objects.get(title = title,author = user)
    comment = ReplyPost.objects.filter(post = post)
    reply = ReplytoReply.objects.filter(post = post)
    user = request.user

    return render(request, 'post.html',{'post':post,'comments':comment,'userLog':request.user.id,'reply':reply,'user':user})

def search(request,problem,methods=['GET']):
    if(request.method == 'GET'):
        title = request.GET['search']
        category = request.GET['category']
        posts = Posts.objects.filter(title__istartswith = title)
        vote = Votes.objects.filter(user = request.user.id)
        for p in posts:
            for v in vote:
                if p.id == v.post.id:
                    if v.vote == "upvote":
                        p.vote = "upvote"
                    elif v.vote == "downvote":
                        p.vote = "downvote"
        user = request.user
        return render(request,'Category.html',{'problem':problem,'posts':posts,'votes':vote,'user':user})

def searchMyIdeas(request,methods=['GET']):
    if  request.method == 'GET':
        title = request.GET['search']
        user = request.user
        post = Posts.objects.filter(title__istartswith = title, author_id = request.user.id)
        return render(request, 'myIdeas.html',{'posts':post,'user':user})

def mySort(request,methods=['GET']):
    if(request.method == 'GET'):
        sort = request.GET['sortBy']
        user = request.user
        if sort == 'Name':
            post = Posts.objects.filter(author_id = request.user.id).order_by('title')
        elif sort == 'Top Rated':
            post = Posts.objects.filter(author_id = request.user.id).order_by('-rating')
        elif sort == 'Date':
            post = Posts.objects.filter(author_id = request.user.id).order_by('-date_posted')

        return render(request, 'myIdeas.html',{'posts':post,'user':user})

def sort(request,problem,methods=['GET']):
    if(request.method == 'GET'):
        sort = request.GET['sortBy']
        user = request.user
        if sort == 'Name':
            post = Posts.objects.filter(category = problem).order_by('title')
            vote = Votes.objects.filter(user = request.user.id)
            for p in post:
                for v in vote:
                    if p.id == v.post.id:
                        if v.vote == "upvote":
                            p.vote = "upvote"
                        elif v.vote == "downvote":
                            p.vote = "downvote"
        elif sort == 'Top Rated':
            post = Posts.objects.filter(category = problem).order_by('-rating')
            vote = Votes.objects.filter(user = request.user.id)
            for p in post:
                for v in vote:
                    if p.id == v.post.id:
                        if v.vote == "upvote":
                            p.vote = "upvote"
                        elif v.vote == "downvote":
                            p.vote = "downvote"
        elif sort == 'Date':
            post = Posts.objects.filter(category = problem).order_by('date_posted')
            vote = Votes.objects.filter(user = request.user.id)
            for p in post:
                for v in vote:
                    if p.id == v.post.id:
                        if v.vote == "upvote":
                            p.vote = "upvote"
                        elif v.vote == "downvote":
                            p.vote = "downvote"
        return render(request, 'Category.html',{'problem':problem,'posts':post,'votes':vote,'userLog':request.user.id,'user':user})

def comment(request,title,user,methods=['GET']):
    if  request.method == 'GET':
        comment = request.GET['comment']
        post = Posts.objects.get(title = title,author = user)
        userLog = request.user
        theComment = ReplyPost(post = post,author = request.user,reply = comment)
        theComment.save()

        return render(request, 'comment.html',{'user':userLog , 'reply':comment})

def reply(request,title,user,methods=['GET']):
    if  request.method == 'GET':
        comment = request.GET['comment']
        replyText = request.GET['reply']
        author = request.GET['author']
        userLog = request.user
        post = Posts.objects.get(title = title,author = user)
        user = User.objects.get(username = author)
        reply = ReplyPost.objects.get(post = post,author = user, reply = comment)
        theReply = ReplytoReply(post = post,replyToPost = reply,author = request.user,replyToComment = replyText)
        theReply.save()

        return render(request, 'reply.html',{'user':userLog , 'reply':replyText})

def uComment(request,title,user,methods=['GET']):
    updatedComment = request.GET['uComment']
    comment = request.GET['comment']
    author = request.GET['author']
    post = Posts.objects.get(title = title,author = user)
    user = User.objects.get(username = author)
    reply = ReplyPost.objects.get(post = post,author = user, reply = comment)
    reply.reply = updatedComment
    reply.save()

    return redirect('./post_page')

def dComment(request,title,user,methods=['GET']):
    comment = request.GET['comment']
    author = request.GET['author']
    post = Posts.objects.get(title = title,author = user)
    user = User.objects.get(username = author)
    reply = ReplyPost.objects.filter(post = post,author = user, reply = comment)
    reply.delete()

    return redirect('./post_page')

def dReply(request,title,user,methods=['GET']):
    comment = request.GET['comment']
    author = request.GET['author']
    post = Posts.objects.get(title = title,author = user)
    user = User.objects.get(username = author)
    authorC = request.GET['authorC']
    authorComment = User.objects.get(username = authorC)
    commentC = request.GET['commentC']
    theComment = ReplyPost.objects.get(post = post,author = authorComment,reply = commentC)
    reply = ReplytoReply.objects.filter(post = post,author = user, replyToComment = comment, replyToPost = theComment)
    reply.delete()

    return redirect('./post_page')

def changePic(request,methods=['POST']):
    if request.method == 'POST':
        user = User.objects.get(id = request.user.id)
        userPic = Users.objects.get(user = user)
        userPic.pic = request.FILES['picture']
        userPic.save()
    
    return redirect('./dashboard')

def report(request,category,title,user,methods=['GET']):
    if request.method == 'GET':
        reason = request.GET['reason']
        user = User.objects.get(username = user)
        post = Posts.objects.get(title = title,category = category, author_id = user)
        report = Reports(post = post, user = request.user,offence = reason)
        report.save()

    return redirect('./post_page')        

def sendMessage(request,category,title,user,methods=['POST']):
    if request.method == "POST":
        entity = Users(id = request.user.id)
        subject = "PinoiseApp Post(" + title +", " + category + ", " + user + ")" 
        message = request.POST['message']
        fromEmail = conf_settings.EMAIL_HOST_USER
        author = User.objects.get(username = user)
        to = [author.email]
        send_mail(subject,message,fromEmail,to,fail_silently=False)

        return redirect('./post_page')