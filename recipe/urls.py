from recipe import views
from django.urls import path

urlpatterns = [
    # path('main/',views.main),
    path('insert/',views.insert, name='insert'),
    # path('show/',views.show, name='show' ),
    path('recommend/',views.recommend, name='recommend'),
    path('video_feed/',views.video_feed, name='video_feed'),
    path('test/',views.test, name='test'),
]