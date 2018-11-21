# -*- coding:utf-8 -*-

from django import forms
import re

def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': "Username",
                                          }
                               ))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': "Password",
                                          }
                               ))
    # Use clean methods to define custom validation rules
    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     # if email_check(username):
    #     #     filter_result = User.objects.filter(email__exact=username)
    #     #     if not filter_result:
    #     #         raise forms.ValidationError("This email does not exist.")
    #     # else:
    #     filter_result = User.objects.filter(username__exact=username)
    #     if not filter_result:
    #         raise forms.ValidationError("You have wrong too many times, Please wait 10 minute!")
    #     return username