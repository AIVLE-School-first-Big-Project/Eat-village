# Generated by Django 3.0.7 on 2022-05-03 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220503_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communityboard',
            name='header',
            field=models.CharField(choices=[('자유게시판', '자유게시판'), ('리뷰게시판', '리뷰게시판'), ('재료나눔게시판', '재료나눔게시판')], max_length=50),
        ),
    ]