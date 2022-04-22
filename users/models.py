from django.db import models
from django.contrib.auth.models import AbstractUser # AbstractUser 불러오기

class User(AbstractUser):
    # username : 아이디
    # first_name : 이름
    # password : 비밀번호
    # email : 이메일

    nickname = models.CharField(max_length=20, blank=True, null=False)
    allergyinfo = models.CharField(max_length=250, blank=True, null=True)
    notpreferred = models.CharField(max_length=250, blank=True, null=True)
    cookingmethod = models.CharField(max_length=250, blank=True, null=True)
    preferredcategory_1 = models.CharField(max_length=250, blank=True, null=True)
    preferredcategory_2 = models.CharField(max_length=250, blank=True, null=True)
    cookingtime = models.CharField(max_length=250, blank=True, null=True)