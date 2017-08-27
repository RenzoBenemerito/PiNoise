from django.shortcuts import render, redirect
from . models import Users,Posts,Category,Votes
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
        return render(request,'dashboard.html',{'user':fName})
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
    posts = Posts.objects.filter(category=problem,votes__post__isnull=True).values()
    vote = Votes.objects.filter(user = request.session['id'])
    print(posts)
    return render(request,'Category.html',{'problem':problem,'posts':posts,'votes':vote,'userLog':request.session['id']})

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
        print(url)
        return redirect(url)

def idea(request):
    posts = Posts.objects.filter(author_id=request.session['id'])
    return render(request,'myIdeas.html',{'posts':posts})

def deletePost(request,methods=['GET']):
    title = request.GET['title']
    posts = Posts.objects.filter(title = title, author_id = request.session['id'])
    posts.delete()
    return redirect('./')

def settings(request):
    return render(request, 'settings.html')

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
        print('failed')
    
    return redirect('./')

def postPage(request,user,title):
    post = Posts.objects.get(title = title,author = user)
    return render(request, 'post.html',{'post':post,'userLog':request.session['id']})

def search(request,problem,methods=['GET']):
    if(request.method == 'GET'):
        title = request.GET['search']
        category = request.GET['category']
        post = Posts.objects.filter(title__istartswith = title,category = category)
        vote = Votes.objects.filter(user = request.session['id'])
        return render(request, 'Category.html',{'problem':problem,'posts':post,'votes':vote,'userLog':request.session['id']})

def sort(request,problem,methods=['GET']):
    if(request.method == 'GET'):
        category = request.GET['category']
        sort = request.GET['sortBy']
        if sort == 'Name':
            post = Posts.objects.filter(category = category).order_by('title')
            vote = Votes.objects.filter(user = request.session['id'])
        elif sort == 'Top Rated':
            post = Posts.objects.filter(category = category).order_by('-rating')
            vote = Votes.objects.filter(user = request.session['id'])
        elif sort == 'Date':
            post = Posts.objects.filter(category = category).order_by('-date_posted')
            vote = Votes.objects.filter(user = request.session['id'])

        return render(request, 'Category.html',{'problem':problem,'posts':post,'votes':vote,'userLog':request.session['id']})