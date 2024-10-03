from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(required=True)
    favorite_movie = forms.CharField(required=True, max_length=255)
    avatar = forms.ImageField(required=False)  # make it optional

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'birth_date', 'favorite_movie', 'password1', 'password2', 'avatar']
