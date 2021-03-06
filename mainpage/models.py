from users.models import *
from django.db import models

class recipe_data(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    num = models.BigIntegerField()
    explan = models.TextField(null=True) # 레시피 조리순서
    title = models.CharField(max_length=255) # 레시피 이름
    ingre = models.TextField() # 식재료
    amount = models.CharField(max_length=10) # 레시피 양
    cook_time = models.CharField(max_length=10) # 조리시간
    level = models.CharField(max_length=20) # 레시피 난이도
    url = models.TextField() # 레시피 설명
    tag = models.CharField(max_length=20, null=True) # 레시피 태그
    category_1 = models.CharField(max_length=20) # 카테고리_1
    category_2 = models.CharField(max_length=20) # 카테고리_2
    method = models.CharField(max_length=20) # 조리방법

    class Meta:
        managed = False
    
    
    # def __str__(self):
        # return self.title
class user_ingre(models.Model):
    # recipe_id = models.AutoField(primary_key=True)
    ingre = models.TextField()

class Userbookmarkrecipe(models.Model):
    bookmarkid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userid', blank=True, null=True)
    recipeid = models.ForeignKey(recipe_data, models.DO_NOTHING, db_column='recipeid', blank=True, null=True)
    # 0 : 알림 확인 안함 , 1 : 알림 확인
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userbookmarkrecipe'