from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^dashboard$',views.dash,name='dash'),
    url(r'^myIdeas/$',views.idea,name='idea'),
    url(r'^settings/$',views.settings,name='settings'),
    url(r'^myIdeas/delete$',views.deletePost,name='deletePost'),
    url(r'^login$',views.login,name='login'),
    url(r'^dashboard/logout$',views.logout,name='logout'),
    url(r'pPage/(?P<problem>.*)/$',views.problemPage,name='problemPage'),
    url(r'^(?P<problem>.*)/addPost$',views.postIdea,name='postIdea'),
    url(r'^.*/(?P<problem>.*)/search$',views.search,name='search'),
    url(r'^.*/mySearch$',views.searchMyIdeas,name='searchMyIdeas'),
    url(r'^.*/mySort$',views.mySort,name='mySort'),
    url(r'^.*/(?P<problem>.*)/sort$',views.sort,name='sort'),
    url(r'^.*/(?P<user>.*)/(?P<title>.*)/post_page$',views.postPage,name='postPage'),
    url(r'^.*/(?P<titleBefore>.*)/updatePost$',views.updateIdea,name='updateIdea'),
    url(r'^passReset$',views.passreset,name='passreset'),
    url(r'^.*/vote$',views.vote,name='vote'),
    ]
