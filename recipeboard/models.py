# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from recipeboard.utils import upload_image

class User(models.Model):
    userid = models.AutoField(db_column='userID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    allergyinfo = models.CharField(max_length=250, blank=True, null=True)
    notpreferred = models.CharField(max_length=250, blank=True, null=True)
    cookingmethod = models.CharField(max_length=250, blank=True, null=True)
    preferredcategory_1 = models.CharField(max_length=250, blank=True, null=True)
    preferredcategory_2 = models.CharField(max_length=250, blank=True, null=True)
    cookingtime = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'USER'

class Recipeboard(models.Model):
    boardid = models.AutoField(db_column='boardID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    title = models.CharField(max_length=50)
    ingredient = models.CharField(max_length=2000)
    detail = models.CharField(max_length=5000)
    view = models.IntegerField()
    recommended = models.IntegerField()
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'RECIPEBOARD'

class Recipephoto(models.Model):
    photoid = models.AutoField(db_column='photoID', primary_key=True)  # Field name made lowercase.
    boardid = models.ForeignKey(Recipeboard, models.DO_NOTHING, db_column='boardID')  # Field name made lowercase.
    photo = models.ImageField(upload_to=upload_image)
    
    class Meta:
        managed = True
        db_table = 'RECIPEPHOTO'

class Recipecomment(models.Model):
    commentid = models.AutoField(db_column='commentID', primary_key=True)  # Field name made lowercase.
    boardid = models.ForeignKey(Recipeboard, models.DO_NOTHING, db_column='boardID')  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    parentcommentid = models.IntegerField(db_column='parentcommentID', blank=True, null=True)  # Field name made lowercase.
    detail = models.CharField(max_length=500)
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'RECIPECOMMENT'


class Recipedata(models.Model):
    recipeid = models.IntegerField(db_column='recipeID', primary_key=True)  # Field name made lowercase.
    recipename = models.CharField(max_length=255)
    cookingmethod = models.CharField(max_length=255)
    category_1 = models.CharField(max_length=255)
    foodtype = models.CharField(max_length=255)
    category_2 = models.CharField(max_length=255)
    detail = models.CharField(max_length=5000)
    ingredient = models.CharField(max_length=5000)
    amount = models.CharField(max_length=20)
    time = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'RECIPEDATA'


class Communityboard(models.Model):
    boardid = models.AutoField(db_column='boardID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    title = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20)
    detail = models.CharField(max_length=5000)
    photo = models.CharField(max_length=50, blank=True, null=True)
    view = models.IntegerField()
    liked = models.IntegerField()
    time = models.DateTimeField()
    location = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'COMMUNITYBOARD'


class Communitycomment(models.Model):
    commentid = models.AutoField(db_column='commentID', primary_key=True)  # Field name made lowercase.
    boardid = models.ForeignKey(Communityboard, models.DO_NOTHING, db_column='boardID')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    parentcommentid = models.IntegerField(db_column='parentcommentID', blank=True, null=True)  # Field name made lowercase.
    detail = models.CharField(max_length=500)
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'COMMUNITYCOMMENT'

class Userbookmark(models.Model):
    bookmarkid = models.AutoField(db_column='bookmarkID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    recipeid = models.ForeignKey(Recipedata, models.DO_NOTHING, db_column='recipeID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'USERBOOKMARK'

class Userlike(models.Model):
    likeid = models.AutoField(db_column='bookmarkID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    boardid = models.ForeignKey(Recipeboard, models.DO_NOTHING, db_column='boardID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'USERLIKE'