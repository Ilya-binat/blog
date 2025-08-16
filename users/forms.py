from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus':True,'placeholder':'Login'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Password'})
    )
    class Meta:
        model = User
        fields = ['username','password']


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus':True, 'placeholder':'Create username'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Create password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Confirm password'})
    )
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
