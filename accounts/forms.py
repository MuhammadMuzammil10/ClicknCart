from django import forms
from accounts.models import User


class CustomSignupForm(forms.Form):
    print("CustomSignupForm Runs")

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']