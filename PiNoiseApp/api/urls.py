from django.conf.urls import url
from . import views
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^categories', views.categoryList.as_view()),
    url(r'^(?P<category>.*)/problem-page', views.CategoryListView.as_view()),
    url(r'^user_register$', views.UserCreateView.as_view()),
    url(r'^user_login$', views.UserLogInView.as_view()),
    url(r'^(?P<category>.*)/problem-page/post$', views.PostCreateView.as_view()),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)