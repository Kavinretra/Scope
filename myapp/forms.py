from django import forms
from .models import *
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=Registration
        # fields='__all__'
        exclude=['is_active']
        widgets={'date_of_birth':forms.DateInput(attrs={'type': 'date','class':'form-control','style':'width : 300px'}),
                 'first_name':forms.TextInput(attrs={'placeholder':'Enter your first name','class':'form-control','style':'width : 300px'}),
                 'last_name':forms.TextInput(attrs={'placeholder':'Enter your last name','class':'form-control','style':'width : 300px'}),
                 'gender':forms.Select(attrs={'class':'form-select','style':'width : 300px'}),
                 'email':forms.EmailInput(attrs={'placeholder':'Enter your email address','class':'form-control','style':'width : 300px'}),
                 'phone_number':forms.NumberInput(attrs={'placeholder':'Enter your phone number','class':'form-control','style':'width : 300px'}),
                 'country':forms.TextInput(attrs={'placeholder':'Enter your country','class':'form-control','style':'width : 300px'}),
                 'state':forms.TextInput(attrs={'placeholder':'Enter your state','class':'form-control','style':'width : 300px'}),
                 'city':forms.TextInput(attrs={'placeholder':'Enter your city','class':'form-control','style':'width : 300px'}),
                 'upload_avatar':forms.FileInput(attrs={'class':'form-control','style':'width : 300px'}),
                 'hobbies':forms.TextInput(attrs={'placeholder':'Enter your hobbies','class':'form-control','style':'width : 300px'})}

class RegisterNow(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email']

        widgets={
                 'email':forms.EmailInput(attrs={'placeholder':'Enter your email address','class':'form-control','style':'width : 300px'}),
                 'username':forms.TextInput(attrs={'placeholder':'Enter your username','class':'form-control','style':'width : 300px'}),
        
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your username','class':'form-control','style':'width : 300px'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your password','class':'form-control','style':'width : 300px'}))


class ForgetPasswordForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter your email address','class':'form-control','style':'width : 300px'}))

class ChangePasswordForm(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your old password','class':'form-control','style':'width : 300px'}))
    new_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your new password','class':'form-control','style':'width : 300px'}))



class ContactForm(forms.Form):
    name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your name','class':'form-control','style':'width : 300px'}))
    phone_number=forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'Enter your phone number','class':'form-control','style':'width : 300px'}))
    