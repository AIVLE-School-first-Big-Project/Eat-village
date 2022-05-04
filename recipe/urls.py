from xml.etree.ElementInclude import include
from django.contrib import admin
from recipe import views
from django.urls import path,include

urlpatterns = [
    # path('main/',views.main),
    path('insert/',views.insert, name='insert'),
    # path('show/',views.show, name='show' ),
    path('recommend/',views.recommend, name='recommend'),
    path('video_feed/',views.video_feed, name='video_feed'),
    path('test/',views.test, name='test'),
]