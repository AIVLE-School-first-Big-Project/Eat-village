from django import forms
from users.models import Recipeboard, Recipeboardimage, Recipecomment

class Recipeboardform(forms.ModelForm):
    class Meta:
        model = Recipeboard
        fields = ['title', 'ingredient', 'detail']

        labels = {
            'title' : '제목',
            'ingredient' : '재료',
            'detail' : '내용',
        }

        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'ingredient' : forms.Textarea(attrs={'class':'form-control', 'rows':5}),
            'detail' : forms.Textarea(attrs={'class':'form-control', 'rows':10}),
        }

class Recipeboardimageform(forms.ModelForm):
    class Meta:
        model = Recipeboardimage
        fields = ['image']

        labels = {'image' : '사진'}

# Imageformset = forms.inlineformset_factory(Recipeboard, Recipeboardimage, form=Recipeboardimageform, extra=3)

class Recipecommentform(forms.ModelForm):
    class Meta:
        model = Recipecomment
        fields= ['detail']
        labels = {
            'detail': '댓글'
        }
        widgets = {
            'detail': forms.Textarea(attrs={'class':'form-control','rows':3})
        }