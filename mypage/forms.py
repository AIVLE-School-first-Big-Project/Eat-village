from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django import forms
from users.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['nickname', 'allergyinfo', 'address']
        # fields = ['nickname', 'allergyinfo', 'address', 'notpreferred', 'preferredcategory_1', 'preferredcategory_2']

class UserWriteForm(forms.ModelForm):
    class Meta:
        model = Communityboard
        fields = '__all__'