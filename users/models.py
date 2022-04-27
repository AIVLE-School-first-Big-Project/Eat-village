from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser	# AbstractUser 불러오기

class User(AbstractUser):
    allergyinfo= models.CharField(max_length=20, default="") #알레르기체크박스
    address = models.CharField(max_length=50, null=True) # 주소
    confirm_password = models.CharField(max_length=20)
                     
