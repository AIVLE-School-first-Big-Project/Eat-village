from django.urls import path
from communityboard.views import *

app_name = 'communityboard'
urlpatterns = [
    path('', communityboard_index, name='communityboard_index'),
    path('<int:boardid>', communityboard_detail, name='communityboard_detail'),
    path('create', communityboard_create, name='communityboard_create'),
    path('update/<int:boardid>', communityboard_update, name='communityboard_update'),
    path('delete/<int:boardid>', communityboard_delete, name='communityboard_delete'),
    path('<int:boardid>/<int:commentid>', communityboard_comment, name='communityboard_comment'),
    path('commentdelete/<int:commentid>', communitycomment_delete, name='communitycomment_delete'),
    ]   
