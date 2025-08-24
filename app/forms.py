from django import forms
from .models import * 

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Оставьте Ваш коментарий'}))
    # Django форма позволяет упростить создание объекта модели, иначе говоря создав форму
    # Можно автоматизироать процесс создания комментария
    class Meta:
        model = Comment
        fields = ['body']