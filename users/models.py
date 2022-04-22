from django.db import models
from django.contrib.auth.models import AbstractUser	# AbstractUser 불러오기

class User(AbstractUser):
    test_list = models.CharField(max_length=20, default="") #알레르기체크박스
    ale = models.CharField(max_length=20, null=True) #알레르기
    postcode = models.CharField(max_length=50, null=True) # 우편번호
    address = models.CharField(max_length=50, null=True) # 주소
    detailAddress = models.CharField(max_length=100, null=True) #상세주소
    extraAddress = models.CharField(max_length=50, null=True) #참고항목
    test1 = models.CharField(max_length=50, null=True)

                     
