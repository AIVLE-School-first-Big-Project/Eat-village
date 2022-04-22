from django.urls import path
from . import views
from .views import * 

app_name = 'mypage'

urlpatterns = [
    # path('user/<int:id>/', views.update_user, name = 'update_user'),
    path('main/', views.user_info),
    path('test/', views.home, name='write'),

]