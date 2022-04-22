# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Communityboard(models.Model):
    boardid = models.AutoField(db_column='boardID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20)
    detail = models.CharField(max_length=5000)
    photo = models.CharField(max_length=50, blank=True, null=True)
    view = models.IntegerField()
    liked = models.IntegerField()
    time = models.DateTimeField()
    location = models.CharField(max_length=20)
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COMMUNITYBOARD'


class Communitycomment(models.Model):
    commentid = models.AutoField(db_column='commentID', primary_key=True)  # Field name made lowercase.
    parentcommentid = models.IntegerField(db_column='parentcommentID', blank=True, null=True)  # Field name made lowercase.
    detail = models.CharField(max_length=500)
    title = models.DateTimeField()
    boardid = models.ForeignKey(Communityboard, models.DO_NOTHING, db_column='boardID')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COMMUNITYCOMMENT'


class Recipeboard(models.Model):
    boardid = models.AutoField(db_column='boardID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=50)
    ingredient = models.CharField(max_length=2000)
    detail = models.CharField(max_length=5000)
    view = models.IntegerField()
    recommended = models.IntegerField()
    time = models.DateTimeField()
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RECIPEBOARD'


class Recipecomment(models.Model):
    commentid = models.AutoField(db_column='commentID', primary_key=True)  # Field name made lowercase.
    parentcommentid = models.IntegerField(db_column='parentcommentID', blank=True, null=True)  # Field name made lowercase.
    detail = models.CharField(max_length=500)
    time = models.DateTimeField()
    boardid = models.ForeignKey(Recipeboard, models.DO_NOTHING, db_column='boardID')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.

    class Meta:
        managed = False
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
        managed = False
        db_table = 'RECIPEDATA'


class Recipephoto(models.Model):
    photoid = models.AutoField(db_column='photoID', primary_key=True)  # Field name made lowercase.
    photo = models.CharField(max_length=100)
    boardid = models.ForeignKey(Recipeboard, models.DO_NOTHING, db_column='boardID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RECIPEPHOTO'


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
    name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'USER'


class Userbookmark(models.Model):
    bookmarkid = models.AutoField(db_column='bookmarkID', primary_key=True)  # Field name made lowercase.
    recipeid = models.ForeignKey(Recipedata, models.DO_NOTHING, db_column='recipeID')  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USERBOOKMARK'


class Userlike(models.Model):
    bookmarkid = models.AutoField(db_column='bookmarkID', primary_key=True)  # Field name made lowercase.
    boardid = models.ForeignKey(Recipeboard, models.DO_NOTHING, db_column='boardID')  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USERLIKE'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
