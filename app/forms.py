from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app import models


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "avatar")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        profile = models.Profile(user=user)
        if commit:
            user.save()
            profile.save()
        return user
