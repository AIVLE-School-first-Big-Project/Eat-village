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
    location = models.CharField(max_length=250)

    class Meat:
        managed = False

class Communityboard(models.Model):
    boardid = models.AutoField(db_column='boardID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    header = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20)
    detail = models.CharField(max_length=5000)
    view = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'COMMUNITYBOARD'


class Communityboardimage(models.Model):
    photoid = models.AutoField(db_column='photoID', primary_key=True)  # Field name made lowercase.
    boardid = models.ForeignKey('Recipeboard', models.DO_NOTHING, db_column='boardID')  # Field name made lowercase.
    image = models.CharField(max_length=200)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'COMMUNITYBOARDIMAGE'


class Communitycomment(models.Model):
    commentid = models.AutoField(db_column='commentID', primary_key=True)  # Field name made lowercase.
    boardid = models.ForeignKey(Communityboard, models.DO_NOTHING, db_column='boardID')  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='id')  # Field name made lowercase.
    parentcommentid = models.IntegerField(db_column='parentcommentID', blank=True, null=True)  # Field name made lowercase.
    detail = models.CharField(max_length=500)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'COMMUNITYCOMMENT'


class Recipeboard(models.Model):
    boardid = models.AutoField(db_column='boardID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='id')  # Field name made lowercase.
    title = models.CharField(max_length=50)
    ingredient = models.CharField(max_length=2000)
    detail = models.CharField(max_length=5000)
    view = models.IntegerField(blank=True, null=True)
    recommended = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'RECIPEBOARD'


class Recipeboardimage(models.Model):
    photoid = models.AutoField(db_column='photoID', primary_key=True)  # Field name made lowercase.
    boardid = models.ForeignKey(Recipeboard, models.DO_NOTHING, db_column='boardID')  # Field name made lowercase.
    image = models.CharField(max_length=200)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'RECIPEBOARDIMAGE'


class Recipecomment(models.Model):
    commentid = models.AutoField(db_column='commentID', primary_key=True)  # Field name made lowercase.
    boardid = models.ForeignKey(Recipeboard, models.DO_NOTHING, db_column='boardID')  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='id')  # Field name made lowercase.
    parentcommentid = models.IntegerField(db_column='parentcommentID', blank=True, null=True)  # Field name made lowercase.
    detail = models.CharField(max_length=500)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'RECIPECOMMENT'


class Recipedata(models.Model):
    recipeid = models.IntegerField(db_column='recipeID', primary_key=True)  # Field name made lowercase.
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
        managed = False
        db_table = 'RECIPEDATA'


class Userbookmarkrecipe(models.Model):
    bookmarkid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='id')  # Field name made lowercase.
    recipeid = models.ForeignKey(Recipedata, models.DO_NOTHING, db_column='recipeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USERBOOKMARKRECIPE'


class Userrecommendedcommunity(models.Model):
    likeid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='id')  # Field name made lowercase.
    boardid = models.ForeignKey(Recipeboard, models.DO_NOTHING, db_column='boardid')

    class Meta:
        managed = False
        db_table = 'USERRECOMMENDEDCOMMUNITY'
