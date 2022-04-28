from django.contrib import admin
from users.models import *

admin.site.register(Recipeboard)
admin.site.register(Recipecomment)
admin.site.register(Recipeboardimage)