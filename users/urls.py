from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'


urlpatterns = [
    path('login/', views.login, name="login"),
    #path('logout/', views.logout, name="logout"),
    path('home/', views.home, name="home"),
    path('back/', views.back, name="back"),
    path('signup/', views.signup, name="signup"),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
]
