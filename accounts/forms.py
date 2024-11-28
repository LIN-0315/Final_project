from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserBank, Account


# user register
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = UserBank
        fields = ['username', 'email', 'phone_number', 'ssn', 'password1', 'password2']


# account create
class AccountCreationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type', 'account_password']
        widgets = {
            'account_password': forms.PasswordInput(attrs={'placeholder': 'Enter account password'}),
        }