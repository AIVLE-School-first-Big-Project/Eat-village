from django import forms
from users.models import Communityboard, Communityboardimage, Communitycomment

class Communityboardform(forms.ModelForm):
    class Meta:
        model = Communityboard
        fields = ['header', 'title', 'detail']

        labels = {
            'header': '',
            'title' : '',
            'detail' : '',
        }

        widgets = {
            'header': forms.Select,
            'title' : forms.TextInput(
                attrs={'placeholder':'제목을 입력해주세요!',
                    'class':'form-control'}
            ),
            'detail' : forms.Textarea(
                attrs={'placeholder':'내용을 입력해주세요!',
                    'class':'form-control', 'rows':20}
            ),
        }

class Communityboardimageform(forms.ModelForm):
    class Meta:
        model = Communityboardimage
        fields = ['image']

        labels = {'image' : ''}

# Imageformset = forms.inlineformset_factory(Communityboard, Communityboardimage, form=Communityboardimageform, extra=3)

class Communitycommentform(forms.ModelForm):
    class Meta:
        model = Communitycomment
        fields= ['detail']
        labels = {
            'detail': ''
        }
        widgets = {
            'detail': forms.Textarea(
                attrs={'placeholder':'댓글을 달아주세요!',
                    'class':'form-control','rows':3})
        }