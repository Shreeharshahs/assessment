from django import forms
from .models import Student

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class StudentForm(forms.Form):
    name = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=100)
    marks = forms.IntegerField(min_value=0, max_value=100)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    c_password = forms.CharField(widget=forms.PasswordInput)
