from django.shortcuts import render, redirect
from . models import Users,Posts,Category,Votes,ReplyPost,ReplytoReply,Reports
from django import forms
from django.http import HttpRequest
from django.http import HttpResponse
from django.contrib import messages

def index(request,methods=['POST']):
    if(request.method == 'POST'):
        fName = request.POST['fName']
        mName = request.POST['mName']
        lName = request.POST['lName']
        email = request.POST['email']
        password = request.POST['pass']

        reg = Users(fName = fName,mName = mName,lName = lName, email = email,password = password)
        reg.save()

    return render(request, 'index.html')

def dash(request):
    if request.session.has_key('id'):
        user = Users.objects.get(id = request.session['id'])
        fName = user.fName + " " + user.mName + " " + user.lName
        category = Category.objects.all()
        return render(request,'dashboard.html',{'user':user,'category':category,'user':user})
    else:
        return HttpResponse("Error 404 You are not logged in.")

def login(request,methods=['POST']): 
    if(request.method == 'POST'):
        email = request.POST['emailLog']
        passLog = request.POST['passLog']
        
        log = Users.objects.get(email = email, password = passLog);
        if log:
            request.session['id'] = log.id
            return redirect('/pinoise/dashboard')
    else:
        return redirect('/pinoise')

def logout(request):
    try:
        request.session.flush()
    except KeyError:
        pass
    return render(request,'index.html')

def problemPage(request,problem):
    posts = Posts.objects.raw('SELECT * FROM pinoiseapp_posts left join pinoiseapp_votes ON pinoiseapp_posts.id=pinoiseapp_votes.post_id WHERE category="{}";'.format(problem))
    vote = Votes.objects.filter(user = request.session['id'])
    user = Users.objects.get(id = request.session['id'])
    fName = user.fName + " " + user.mName + " " + user.lName
    print(user.pic.url)
    return render(request,'Category.html',{'problem':problem,'posts':posts,'votes':vote,'userLog':request.session['id'],'userName':fName,'user':user})

def postIdea(request,problem,methods=['POST']):
    if(request.method == 'POST'):
        title = request.POST['title']
        description = request.POST['ideation']
        category = request.POST['category']
        category1 = Category.objects.get(category=category)
        poster = Users.objects.get(id=request.session['id'])
        fName = poster.fName + " " + poster.mName + " " + poster.lName
        post = Posts(author_id = poster,author = fName,title = title,description = description,category_id = category1,category = category1.category)
        post.save()
    
        return redirect('./')

def updateIdea(request,titleBefore,methods=['POST']):
    if(request.method == 'POST'):
        title = request.POST['title']
        description = request.POST['ideation']
        category = request.POST['category']
        category1 = Category.objects.get(category=category)
        poster = Users.objects.get(id=request.session['id'])
        post = Posts.objects.get(author_id = poster,title = titleBefore,category_id = category1,category = category1.category)
        post.title = title
        post.description = description
        post.save()
        url = '../'+title +'/post_page'
        return redirect(url)

def idea(request):
    user = Users.objects.get(id = request.session['id'])
    fName = user.fName + " " + user.mName + " " + user.lName
    posts = Posts.objects.filter(author_id=request.session['id'])
    return render(request,'myIdeas.html',{'posts':posts,'user':user})

def deletePost(request,methods=['GET']):
    title = request.GET['title']
    posts = Posts.objects.filter(title = title, author_id = request.session['id'])
    posts.delete()
    return redirect('./')

def settings(request):
    user = Users.objects.get(id = request.session['id'])
    fName = user.fName + " " + user.mName + " " + user.lName
    return render(request, 'settings.html',{'user':user})

def passreset(request,methods=['POST']):
    user = Users.objects.get(id = request.session['id'])
    oldPass = request.POST['pass']
    newPass = request.POST['pass1']
    newPass2 = request.POST['pass2']

    if oldPass == user.password and newPass == newPass2:
        user.password = newPass
        user.save()
    
    return redirect('./')

def vote(request,methods=['GET']):
    title = request.GET['title']
    kind = request.GET['kind']
    author = request.GET['author']
    post = Posts.objects.get(title = title,author = author)
    try:
        check = Votes.objects.get(user = request.session['id'], post = post.id)
    except Votes.DoesNotExist:
        check = None
    if check is None:
        voter = Votes(user = Users.objects.get(id = request.session['id']),post = post,vote = kind)
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
    user = Users.objects.get(id = request.session['id'])
    fName = user.fName + " " + user.mName + " " + user.lName

    return render(request, 'post.html',{'post':post,'userLog':request.session['id'],'comments':comment,'reply':reply,'user':user})

def search(request,problem,methods=['GET']):
    if(request.method == 'GET'):
        title = request.GET['search']
        category = request.GET['category']
        posts = Posts.objects.raw('SELECT * FROM pinoiseapp_posts left join pinoiseapp_votes ON pinoiseapp_posts.id=pinoiseapp_votes.post_id WHERE category="{}" && pinoiseapp_posts.title LIKE CONCAT("%%","{}","%%");'.format(problem,title))
        user = Users.objects.get(id = request.session['id'])
        fName = user.fName + " " + user.mName + " " + user.lName
        return render(request,'Category.html',{'problem':problem,'posts':posts,'votes':vote,'userLog':request.session['id'],'user':user})

def searchMyIdeas(request,methods=['GET']):
    if  request.method == 'GET':
        title = request.GET['search']
        user = Users.objects.get(id = request.session['id'])
        fName = user.fName + " " + user.mName + " " + user.lName
        post = Posts.objects.filter(title__istartswith = title, author_id = request.session['id'])
        return render(request, 'myIdeas.html',{'posts':post,'user':user})

def mySort(request,methods=['GET']):
    if(request.method == 'GET'):
        sort = request.GET['sortBy']
        if sort == 'Name':
            post = Posts.objects.filter(author_id = request.session['id']).order_by('title')
        elif sort == 'Top Rated':
            post = Posts.objects.filter(author_id = request.session['id']).order_by('-rating')
        elif sort == 'Date':
            post = Posts.objects.filter(author_id = request.session['id']).order_by('-date_posted')

        return render(request, 'myIdeas.html',{'posts':post})

def sort(request,problem,methods=['GET']):
    if(request.method == 'GET'):
        sort = request.GET['sortBy']
        if sort == 'Name':
            post = Posts.objects.filter(category = problem).order_by('title')
            vote = Votes.objects.filter(user = request.session['id'])
        elif sort == 'Top Rated':
            post = Posts.objects.filter(category = problem).order_by('-rating')
            vote = Votes.objects.filter(user = request.session['id'])
        elif sort == 'Date':
            post = Posts.objects.filter(category = problem).order_by('date_posted')
            vote = Votes.objects.filter(user = request.session['id'])

        return render(request, 'Category.html',{'problem':problem,'posts':post,'votes':vote,'userLog':request.session['id']})

def comment(request,title,user,methods=['GET']):
    if  request.method == 'GET':
        comment = request.GET['comment']
        post = Posts.objects.get(title = title,author = user)
        theComment = ReplyPost(post = post,author = Users.objects.get(id=request.session['id']),reply = comment)
        theComment.save()

        return redirect('./post_page')

def reply(request,title,user,methods=['GET']):
    if  request.method == 'GET':
        comment = request.GET['comment']
        replyText = request.GET['reply']
        author = request.GET['author']
        post = Posts.objects.get(title = title,author = user)
        name = author.split(' ');
        user = Users.objects.get(fName = name[0],mName = name[1],lName = name[2])
        reply = ReplyPost.objects.get(post = post,author = user, reply = comment)
        theReply = ReplytoReply(post = reply.post,replyToPost = reply,author = Users.objects.get(id=request.session['id']),replyToComment = replyText)
        theReply.save()

        return redirect('./post_page')

def dComment(request,title,user,methods=['GET']):
    comment = request.GET['comment']
    author = request.GET['author']
    post = Posts.objects.get(title = title,author = user)
    name = author.split(' ');
    user = Users.objects.get(fName = name[0],mName = name[1],lName = name[2])
    reply = ReplyPost.objects.get(post = post,author = user, reply = comment)
    reply.delete()

    return redirect('./post_page')

def dReply(request,title,user,methods=['GET']):
    comment = request.GET['comment']
    author = request.GET['author']
    post = Posts.objects.get(title = title,author = user)
    name = author.split(' ');
    user = Users.objects.get(fName = name[0],mName = name[1],lName = name[2])
    reply = ReplytoReply.objects.get(post = post,author = user, replyToComment = comment)
    reply.delete()

    return redirect('./post_page')

def changePic(request,methods=['POST']):
    if request.method == 'POST':
        user = Users.objects.get(id=request.session['id'])
        user.pic = request.FILES['picture']
        user.save()
    
    return redirect('./dashboard')

def report(request,category,title,user,methods='GET'):
    if request.method == 'GET':
        reason = request.GET['reason']
        name = user.split(' ');
        user = Users.objects.get(fName = name[0],mName = name[1],lName = name[2])
        post = Posts.objects.get(title = title,category = category, author_id = user)
        report = Reports(post = post, user = Users.objects.get(id=request.session['id']),offence = reason)
        report.save()

    return redirect('./post_page')        
