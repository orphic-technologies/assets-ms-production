from django import forms
from .models import User


class LoginForm(forms.Form):

    username = forms.EmailField(
        error_messages={"required": ""},
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter username",
                "name": "username",
                "id": "username",
                "class": "form-control",
            }
        ),
    )

    password = forms.CharField(
        error_messages={"required": ""},
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter password",
                "name": "password",
                "id": "userpassword",
                "class": "form-control",
            }
        ),
    )
    rememberMe = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={
                "name": "remember-me",
                "id": "remember-me",
                "class": "agree-term",
            }
        ),
    )


class UserAddForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "current_position",
            "access",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "username",
                    "name": "name",
                    "id": "name",
                    "class": "name",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "placeholder": "password",
                    "name": "pass",
                    "id": "pass",
                    "class": "form-control form-control-sm mb-2 password",
                }
            ),
            "current_position": forms.EmailInput(
                attrs={
                    "placeholder": "current_position",
                    "name": "position",
                    "id": "position",
                    "class": "position",
                }
            ),
            "access": forms.TextInput(
                attrs={
                    "placeholder": "access",
                    "id": "access",
                    "class": "access",
                }
            ),
        }
