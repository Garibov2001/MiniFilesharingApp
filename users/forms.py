from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("Bu email artiq movcuddur")
       return email
    
    def clean_username(self):
       username = self.cleaned_data.get('username')
       if User.objects.filter(username=username).exists():
            raise ValidationError("Bu username artiq movcuddur")
       return username