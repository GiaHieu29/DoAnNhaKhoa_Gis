from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class DangKyForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ("username", "email") 


class DangNhapForm(forms.Form):
    username = forms.CharField(label="Tên đăng nhập", max_length=100)
    password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput)