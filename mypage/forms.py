from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from users.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['nickname', 'allergyinfo', 'location']
        # fields = ['nickname', 'allergyinfo', 'location', 'notpreferred', 'preferredcategory_1', 'preferredcategory_2']