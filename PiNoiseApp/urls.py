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
    url(r'^passReset$',views.passreset,name='passreset'),
    ]
