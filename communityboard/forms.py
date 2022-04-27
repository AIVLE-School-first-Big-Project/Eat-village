from django import forms
from users.models import Communityboard, Communityboardimage, Communitycomment

class Communityboardform(forms.ModelForm):
    class Meta:
        model = Communityboard
        fields = ['header', 'title', 'detail']

        labels = {
            'header': '게시판선택',
            'title' : '제목',
            'detail' : '내용',
        }

        widgets = {
            'header': forms.Select,
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'detail' : forms.Textarea(attrs={'class':'form-control', 'rows':10}),
        }

class Communityboardimageform(forms.ModelForm):
    class Meta:
        model = Communityboardimage
        fields = ['image']

        labels = {'image' : '사진'}

# Imageformset = forms.inlineformset_factory(Communityboard, Communityboardimage, form=Communityboardimageform, extra=3)

class Communitycommentform(forms.ModelForm):
    class Meta:
        model = Communitycomment
        fields= ['detail']
        labels = {
            'detail': '댓글'
        }
        widgets = {
            'detail': forms.Textarea(attrs={'class':'form-control','rows':3})
        }