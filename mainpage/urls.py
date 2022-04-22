from django.urls import path
from django.contrib.auth import views as auth_views
from mainpage import views

app_name = 'mainpage'
urlpatterns = [
    path('mainpage/', views.main, name='mainpage'),
    path('weather/', views.weather_recomm, name='weather'),
    path('ingred/', views.ingred_recomm, name='ingredient'),
    path('search/', views.recipe_search, name='search'),
]