from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Book


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class DepositForm(forms.Form):
    amount = forms.DecimalField(label="Amount to Deposit")


class ReturnForm(forms.Form):
    book_id = forms.IntegerField(label="Book ID")


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class BorrowBookForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), empty_label=None)


class ReviewForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), empty_label=None)
    text = forms.CharField(widget=forms.Textarea)
    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)])
