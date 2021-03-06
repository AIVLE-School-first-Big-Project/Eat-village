from django.db import models
from django.contrib.auth.models import AbstractUser # AbstractUser 불러오기

class User(AbstractUser):
    # id
    # username : 아이디
    # first_name : 이름
    # password : 비밀번호
    # email : 이메일
    nickname = models.CharField(max_length=20)
    allergyinfo = models.CharField(max_length=250, blank=True, null=True)
    notpreferred = models.CharField(max_length=250, blank=True, null=True)
    cookingmethod = models.CharField(max_length=250, blank=True, null=True)
    preferredcategory_1 = models.CharField(max_length=250, blank=True, null=True)
    preferredcategory_2 = models.CharField(max_length=250, blank=True, null=True)
    cookingtime = models.CharField(max_length=250, blank=True, null=True)
    address = models.CharField(max_length=250, null=True) # 주소
    confirm_password = models.CharField(max_length=200, blank=True, null=True)
    ingre = models.TextField(null=True)

class Communityboard(models.Model):
    boardid = models.AutoField(db_column='boardID', primary_key=True)  
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID', null=True)  
    header = models.CharField(max_length=50, choices=(('자유게시판', '자유게시판'), ('리뷰게시판', '리뷰게시판'), ('재료나눔게시판', '재료나눔게시판')))
    title = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20)
    detail = models.CharField(max_length=5000)
    view = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'COMMUNITYBOARD'


class Communityboardimage(models.Model):
    photoid = models.AutoField(db_column='photoID', primary_key=True)  
    boardid = models.ForeignKey('Communityboard', db_column='boardID', null=True, on_delete=models.CASCADE)  
    image = models.ImageField(upload_to='communityboard/', null=True, verbose_name="")
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'COMMUNITYBOARDIMAGE'


class Communitycomment(models.Model):
    commentid = models.AutoField(db_column='commentID', primary_key=True)  
    boardid = models.ForeignKey(Communityboard, related_name='comments', db_column='boardID', null=True, on_delete=models.CASCADE)  
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID', null=True)  
    parentcommentid = models.IntegerField(db_column='parentcommentID', blank=True, null=True)  
    detail = models.CharField(max_length=500)
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'COMMUNITYCOMMENT'


class Recipeboard(models.Model):
    boardid = models.AutoField(db_column='boardID', primary_key=True)  
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID', null=True)  
    title = models.CharField(max_length=50)
    ingredient = models.CharField(max_length=2000)
    detail = models.CharField(max_length=5000)
    view = models.IntegerField(blank=True, null=True)
    recommended = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'RECIPEBOARD'

class Recipeboardimage(models.Model):
    photoid = models.AutoField(db_column='photoID', primary_key=True)  
    boardid = models.ForeignKey(Recipeboard, db_column='boardID', null=True, on_delete=models.CASCADE)  
    image = models.ImageField(upload_to='recipeboard/', null=True, verbose_name="")
    time = models.DateTimeField()

    def __str__(self):
        return self.name + ": " + str(self.imagefile)

    class Meta:
        managed = True
        db_table = 'RECIPEBOARDIMAGE'


class Recipecomment(models.Model):
    commentid = models.AutoField(db_column='commentID', primary_key=True)  
    boardid = models.ForeignKey(Recipeboard, related_name='comments', db_column='boardID', null=True, on_delete=models.CASCADE)  
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID', null=True)  
    parentcommentid = models.IntegerField(db_column='parentcommentID', blank=True, null=True)  
    detail = models.CharField(max_length=500)
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'RECIPECOMMENT'


class Userrecommendedcommunity(models.Model):
    likeid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID', null=True)  
    boardid = models.ForeignKey(Recipeboard, db_column='boardid', null=True, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'USERRECOMMENDEDCOMMUNITY'

# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


# class UsersUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()
#     nickname = models.CharField(max_length=20)
#     allergyinfo = models.CharField(max_length=250, blank=True, null=True)
#     notpreferred = models.CharField(max_length=250, blank=True, null=True)
#     cookingmethod = models.CharField(max_length=250, blank=True, null=True)
#     preferredcategory_1 = models.CharField(max_length=250, blank=True, null=True)
#     preferredcategory_2 = models.CharField(max_length=250, blank=True, null=True)
#     cookingtime = models.CharField(max_length=250, blank=True, null=True)
#     location = models.CharField(max_length=50)

#     class Meta:
#         managed = True
#         db_table = 'users_user'


# class UsersUserGroups(models.Model):
#     user = models.ForeignKey(UsersUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'users_user_groups'
#         unique_together = (('user', 'group'),)


# class UsersUserUserPermissions(models.Model):
#     user = models.ForeignKey(UsersUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'users_user_user_permissions'
#         unique_together = (('user', 'permission'),)




# class recipe_data(models.Model):
#     recipe_id = models.AutoField(primary_key=True)
#     num =  models.BigIntegerField()
#     explan = models.TextField(null=True) # 레시피 조리순서
#     title = models.CharField(max_length=255) # 레시피 이름
#     ingre = models.TextField() # 식재료
#     amount = models.CharField(max_length=10) # 레시피 양
#     cook_time = models.CharField(max_length=10) # 조리시간
#     level = models.CharField(max_length=20) # 레시피 난이도
#     url = models.TextField() # 레시피 설명
#     tag = models.CharField(max_length=20, null=True) # 레시피 태그
#     category_1 = models.CharField(max_length=20) # 카테고리_1
#     category_2 = models.CharField(max_length=20) # 카테고리_2
#     method = models.CharField(max_length=20) # 조리방법
    
# # class           
#     # def __str__(self):
#         # return self.title

# class user_ingre(models.Model):
#     # recipe_id = models.AutoField(primary_key=True)
#     ingre = models.TextField()


# class userbookmarkrecipe(models.Model):
#     bookmarkid = models.AutoField(primary_key=True)
#     userid = models.ForeignKey(User, models.DO_NOTHING, null=True)  
#     recipeid = models.ForeignKey(recipe_data, null=True, on_delete=models.CASCADE)
#     is_active = models.BooleanField(default=True) 


# class recipe_data(models.Model):
#     recipe_id = models.AutoField(primary_key=True)
#     num =  models.BigIntegerField()
#     explan = models.TextField(null=True) # 레시피 조리순서
#     title = models.CharField(max_length=255) # 레시피 이름
#     ingre = models.TextField() # 식재료
#     amount = models.CharField(max_length=10) # 레시피 양
#     cook_time = models.CharField(max_length=10) # 조리시간
#     level = models.CharField(max_length=20) # 레시피 난이도
#     url = models.TextField() # 레시피 설명
#     tag = models.CharField(max_length=20, null=True) # 레시피 태그
#     category_1 = models.CharField(max_length=20) # 카테고리_1
#     category_2 = models.CharField(max_length=20) # 카테고리_2
#     method = models.CharField(max_length=20) # 조리방법
    
# # class           
#     # def __str__(self):
#         # return self.title

# # class user_ingre(models.Model):
# #     # recipe_id = models.AutoField(primary_key=True)
# #     ingre = models.TextField()


# class Userbookmarkrecipe(models.Model):
#     bookmarkid = models.IntegerField(primary_key=True)
#     userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userid', blank=True, null=True)
#     recipeid = models.ForeignKey(recipe_data, models.DO_NOTHING, db_column='recipeid', blank=True, null=True)
#     is_active = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'userbookmarkrecipe'