from django.conf.urls import url
from . import views
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^dashboard$',views.dash,name='dash'),
    url(r'^myIdeas/$',views.idea,name='idea'),
    url(r'^settings/$',views.settings,name='settings'),
    url(r'^myIdeas/delete$',views.deletePost,name='deletePost'),
    url(r'^login$',views.user_login,name='login'),
    url(r'^dashboard/logout$',views.user_logout,name='logout'),
    url(r'pPage/(?P<problem>.*)/$',views.problemPage,name='problemPage'),
    url(r'^(?P<problem>.*)/addPost$',views.postIdea,name='postIdea'),
    url(r'^.*/(?P<problem>.*)/search$',views.search,name='search'),
    url(r'^.*/mySearch$',views.searchMyIdeas,name='searchMyIdeas'),
    url(r'^.*/mySort$',views.mySort,name='mySort'),
    url(r'^.*/(?P<problem>.*)/sort$',views.sort,name='sort'),
    url(r'^.*/(?P<user>.*)/(?P<title>.*)/post_page$',views.postPage,name='postPage'),
    url(r'^.*/(?P<category>.*)/(?P<user>.*)/(?P<title>.*)/report$',views.report,name='report'),
    url(r'^.*/(?P<category>.*)/(?P<user>.*)/(?P<title>.*)/sendMessage$',views.sendMessage,name='sendMessage'),
    url(r'^.*/(?P<user>.*)/(?P<title>.*)/comment$',views.comment,name='comment'),
    url(r'^.*/(?P<user>.*)/(?P<title>.*)/editComment',views.uComment,name='uComment'),
    url(r'^.*/(?P<user>.*)/(?P<title>.*)/deleteComment$',views.dComment,name='dComment'),
    url(r'^.*/(?P<user>.*)/(?P<title>.*)/editReply$',views.editReply,name='editReply'),
    url(r'^.*/(?P<user>.*)/(?P<title>.*)/deleteReply$',views.dReply,name='dReply'),
    url(r'^.*/(?P<user>.*)/(?P<title>.*)/reply$',views.reply,name='reply'),
    url(r'^.*/(?P<titleBefore>.*)/updatePost$',views.updateIdea,name='updateIdea'),
    url(r'^changePic',views.changePic,name='changePic'),
    url(r'^.*/vote$',views.vote,name='vote'),
    url(r'^categories', views.categoryList.as_view()),
    url(r'^(?P<category>.*)/problem-page', views.CategoryListView.as_view()),
    url(r'^register$', views.UserCreateView.as_view()),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)