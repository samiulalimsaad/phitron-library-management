from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["text"]


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class DepositForm(forms.Form):
    amount = forms.DecimalField(label="Amount to Deposit")


class BorrowForm(forms.Form):
    book_id = forms.IntegerField(label="Book ID")


class ReturnForm(forms.Form):
    book_id = forms.IntegerField(label="Book ID")
