from django.urls import path
from . import views
from .views import * 

app_name = 'mypage'

urlpatterns = [
    path('main/', views.user_info),
    path('test/', views.home, name='write'),
    # path('userDelete/', views.user_delete, name='profile_delete'),
    path('write_list/', views.show_writeList, name='write_list')
]