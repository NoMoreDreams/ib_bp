import re

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=7, help_text="Enter your TUKE login (ab123cd)"
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(
        max_length=254,
        help_text="Enter your TUKE valid email address (name.surname@student.tuke.sk",
    )

    def clean_username(self):
        username = self.cleaned_data["username"]

        # Define the regex pattern for the username format
        pattern = r"^[a-z]{2}\d{3}[a-z]{2}$"

        # Check if the username matches the pattern
        if not re.match(pattern, username):
            raise forms.ValidationError("Invalid username format.")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]

        # Define the desired email prefix
        desired_prefix = "@student.tuke.sk"
        desired_prefix2 = "@tuke.sk"

        # Check if the email has the desired prefix
        if not email.endswith(desired_prefix) and not email.endswith(desired_prefix2):
            raise forms.ValidationError("Invalid email format.")

        return email

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
