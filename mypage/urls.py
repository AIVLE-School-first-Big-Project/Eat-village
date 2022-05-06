from django.urls import path
from . import views
from .views import * 

app_name = 'mypage'

urlpatterns = [
    path('main/', views.user_info, name='main'),
    path('test/', views.home, name='write'),
    path('write_list/', views.show_writeList, name='write_list'),
    path('show_likeList/', views.show_likeList, name='show_likeList'),
    path('show_bookmark/', views.show_bookmark, name="show_bookmark")
]