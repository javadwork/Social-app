from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput({'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput({'class': 'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput({'class': 'form-control'}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput({'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('Your username is already use')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('Your email is already use')
        return email

    # this method is process on Register form with all fields not one fields (password)
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('Your Pass not match!')


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput({'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput({'class': 'form-control'}))
