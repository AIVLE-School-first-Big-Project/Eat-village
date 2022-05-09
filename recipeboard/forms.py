from django import forms
from users.models import Recipeboard, Recipeboardimage, Recipecomment

class Recipeboardform(forms.ModelForm):
    class Meta:
        model = Recipeboard
        fields = ['title', 'ingredient', 'detail']

        labels = {
            'title' : '',
            'ingredient' : '',
            'detail' : '',
        }

        widgets = {
            'title' : forms.TextInput(
                attrs={'placeholder':'제목을 입력해주세요!',
                       'class':'form-control'}
            ),
            'ingredient' : forms.Textarea(
                attrs={'placeholder':'요리에 필요한 재료를 입력해주세요!',
                       'class':'form-control', 'rows':5}
            ),
            'detail' : forms.Textarea(
                attrs={'placeholder':'요리 과정을 자세하게 입력해주세요!',
                       'class':'form-control', 'rows':10}
            ),
        }

class Recipeboardimageform(forms.ModelForm):
    class Meta:
        model = Recipeboardimage
        fields = ['image']

        labels = {'image' : ''}

# Imageformset = forms.inlineformset_factory(Recipeboard, Recipeboardimage, form=Recipeboardimageform, extra=3)

class Recipecommentform(forms.ModelForm):
    class Meta:
        model = Recipecomment
        fields= ['detail']
        labels = {
            'detail': ''
        }
        widgets = {
            'detail': forms.Textarea(
                attrs={'placeholder':'댓글을 달아주세요!',
                    'class':'form-control','rows':3})
        }