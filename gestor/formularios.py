from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    username=forms.CharField(label='Nombre de Usuario')
    email=forms.CharField(label='correo', widget=forms.EmailInput)
    password1=forms.CharField(label='contraseña', widget=forms.PasswordInput)
    password2=forms.CharField(label='Confirme Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User

        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}