from django.urls import path
from mainpage import views

app_name = 'mainpage'
urlpatterns = [
    path('mainpage/', views.main, name='mainpage'),
    path('ingred_recipe/', views.ingred_recomm, name='ingredient_recom'),
    path('search/', views.recipe_search, name='search'),
    path('ingred_result/', views.ingred_result, name='ingredient_result'),
    path('ingred_change/', views.ingred_change  , name='ingredient_change'),
    path('video_feed/',views.video_feed, name='video_feed'),
    # path('test/',views.test, name='test'),
    # path('recipeDetail/', views.recipe_detail, name='recipe_detail'),
    path('recipeDetail/<int:recipe_id>', views.recipe_detail, name='recipe_detail'),
    path('loading/', views.loading, name='loading'), # should be deleted
]
