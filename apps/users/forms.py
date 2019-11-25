__author__ = 'wdz'
__date__ = '2019/10/20 19:44'
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "The Code is wrong"})

class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "The Code is wrong"})

class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

class UploadImageForm(forms.ModelForm):
    class Meta:
        model =UserProfile
        fields = ['image']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'mobile', 'gender', 'address']