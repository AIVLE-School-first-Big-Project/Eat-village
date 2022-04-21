import re
from django.db import models

# Create your models here.
class recipe_data(models.Model):
    # recipe_id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=255) # 레시피 이름
    method = models.CharField(max_length=20) # 조리방법
    type = models.CharField(max_length=20)
    category_1 = models.CharField(max_length=20) # 카테고리_1
    category_2 = models.CharField(max_length=20) # 카테고리_2
    mgt = models.TextField() # 레시피 설명
    igd = models.TextField() # 식재료
    serv = models.CharField(max_length=10)
    cook_time = models.CharField(max_length=10) 

        
    # def __str__(self):
        # return self.title
class user_ingre(models.Model):
    # recipe_id = models.AutoField(primary_key=True)
    ingre = models.TextField()