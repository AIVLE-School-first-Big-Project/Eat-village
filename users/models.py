# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from recipeboard.utils import upload_image
from django.contrib.auth.models import AbstractUser	# AbstractUser 불러오기

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
    location = models.CharField(max_length=250)

class Communityboard(models.Model):
    boardid = models.AutoField(db_column='boardID', primary_key=True)  
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID', null=True)  
    header = models.CharField(max_length=50, choices=(('요리재료게시판', '요리재료게시판'), ('자유게시판', '자유게시판')))
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
    boardid = models.ForeignKey(Communityboard, db_column='boardID', null=True, on_delete=models.CASCADE)  
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
    boardid = models.ForeignKey(Recipeboard, db_column='boardID', null=True, on_delete=models.CASCADE)  
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID', null=True)  
    parentcommentid = models.IntegerField(db_column='parentcommentID', blank=True, null=True)  
    detail = models.CharField(max_length=500)
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'RECIPECOMMENT'


class Recipedata(models.Model):
    recipeid = models.IntegerField(db_column='recipeID', primary_key=True)  
    recipeno = models.CharField(max_length=50)
    recipename = models.CharField(max_length=255)
    ingredient = models.CharField(max_length=5000)
    amount = models.CharField(max_length=20)
    cooktime = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    url = models.CharField(max_length=500)
    tag = models.CharField(max_length=1000)
    cookingmethod = models.CharField(max_length=255)
    category_1 = models.CharField(max_length=255)
    foodtype = models.CharField(max_length=255)
    category_2 = models.CharField(max_length=255)
    detail = models.CharField(max_length=5000)
    time = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'RECIPEDATA'


class Userbookmarkrecipe(models.Model):
    bookmarkid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID', null=True)  
    recipeid = models.ForeignKey(Recipedata, db_column='recipeID', null=True, on_delete=models.CASCADE)  

    class Meta:
        managed = True
        db_table = 'USERBOOKMARKRECIPE'


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
