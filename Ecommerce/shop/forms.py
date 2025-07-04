from django import forms
from django.contrib.auth.forms import UserCreationForm
from shop.models import User
from django.forms import PasswordInput
from shop.models import Category,Product



class SignupForm(UserCreationForm):

    class Meta:
        model=User
        fields=['username','password1','password2','phone','email','first_name','last_name']


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=PasswordInput)


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'



class AddProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['name','image','description','price','stock','category']