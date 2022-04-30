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

class CheckPasswordForm(forms.Form):
    password = forms.CharField(
        label='비밀번호', 
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ), 
    )
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password
        
        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 일치하지 않습니다.')