from django.urls import path
from . import views
from .views import * 

app_name = 'mypage'

urlpatterns = [
    path('main/', views.user_info),
    path('test/', views.home, name='write'),

]