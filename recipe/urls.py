from xml.etree.ElementInclude import include
from django.contrib import admin
from recipe import views
from django.urls import path

urlpatterns = [
    # path('main/',views.main),
    path('insert/',views.insert),
    path('show/',views.show),
    path('recommend/',views.recoommend),
    path('video_feed/',views.video_feed, name='video_feed'),
    
    # path('mypage/', include('mypageapp.urls'))
]