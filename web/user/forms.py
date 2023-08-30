
from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth import get_user_model
from django.forms import CharField, PasswordInput
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
        
        class Meta(UserCreationForm):
            model = User
            fields = ('email', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
        password1 = CharField(label=("Password"), required=False, widget=PasswordInput)
        password2 = CharField(label=("Password confirmation"),  required=False, widget=PasswordInput)

        class Meta:
            model = User
            fields = ('first_name', 'last_name', 'avatar', 'password1', 'password2')

