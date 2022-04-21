from django.urls import path
from recipeboard.views import *

app_name = 'recipeboard'
urlpatterns = [
    path('', recipeboard_index, name='recipeboard_index'),
    path('<int:boardid>', recipeboard_detail, name='recipeboard_detail'),
    path('create', recipeboard_create, name='recipeboard_create'),
    path('update/<int:boardid>', recipeboard_update, name='recipeboard_update'),
    path('delete/<int:boardid>', recipeboard_delete, name='recipeboard_delete'),
    path('<int:boardid>/<int:commentid>', recipeboard_comment, name='recipeboard_comment'),
    path('commentdelete/<int:commentid>', recipecomment_delete, name='recipecomment_delete'),
    
]
