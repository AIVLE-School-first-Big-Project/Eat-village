from django.urls import path
from django.contrib.auth import views as auth_views
from mainpage import views

app_name = 'mainpage'
urlpatterns = [
    path('mainpage/', views.main, name='mainpage'),
    path('weather/', views.weather_recomm, name='weather'),
    path('ingred_recipe/', views.ingred_recomm, name='ingredient_recom'),
    path('search/', views.recipe_search, name='search'),
    path('ingred_result/', views.ingred_result, name='ingredient_result'),
    path('ingred_change/', views.ingred_change, name='ingredient_change'),
]
