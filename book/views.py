from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import (
    BorrowBookForm,
    DepositForm,
    ReturnForm,
    ReviewForm,
    UserProfileForm,
    UserRegistrationForm,
)
from .models import Book, BorrowingHistory, UserAccount


def home(args):
    return redirect("book_list")


def send_deposit_email(user_email, amount):
    subject = "Deposit Confirmation"
    message = render_to_string("emails/deposit_email.html", {"amount": amount})
    send_mail(subject, message, None, [user_email])


def send_borrow_email(user_email, book_title, borrowed_amount):
    subject = "Book Borrowed"
    message = render_to_string(
        "emails/borrow_email.html",
        {"book_title": book_title, "borrowed_amount": borrowed_amount},
    )
    send_mail(subject, message, None, [user_email])


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "books"


class BorrowBookView(FormView):
    template_name = "users/borrow.html"
    form_class = BorrowBookForm
    success_url = reverse_lazy("book_list")

    def form_valid(self, form):
        book_id = self.kwargs["pk"]
        book = Book.objects.get(pk=book_id)

        # Create a borrowing history record
        BorrowingHistory.objects.create(user=self.request.user, book=book)

        messages.success(
            self.request, f"You have borrowed '{book.title}' successfully!"
        )
        return super().form_valid(form)


class ReturnBookView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return redirect("user_profile")


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        # Handle book review logic
        return redirect("book_detail", pk=kwargs["pk"])


class UserRegistrationView(FormView):

    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("book_list")

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        authenticated_user = authenticate(
            self.request, username=username, password=password
        )
        if authenticated_user is not None:
            login(self.request, authenticated_user)
        return super().form_valid(form)


class DepositView(FormView):
    template_name = "users/deposit.html"
    form_class = DepositForm
    success_url = reverse_lazy("success")

    def form_valid(self, form):

        current_user = self.request.user

        try:

            user_account = UserAccount.objects.get(user=current_user)
        except UserAccount.DoesNotExist:

            user_account = UserAccount.objects.create(
                user=current_user, deposit_amount=0
            )

        amount = form.cleaned_data["amount"]
        user_account.deposit_amount += amount
        user_account.save()
        print(current_user.email)

        send_deposit_email(current_user.email, amount)

        messages.success(self.request, "Deposit successful!")

        return super().form_valid(form)


class DepositSuccessView(TemplateView):
    template_name = "users/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Deposit successful!"
        return context


class AddReviewView(FormView):
    template_name = "users/add_review.html"
    form_class = ReviewForm
    success_url = reverse_lazy("book_list")

    def form_valid(self, form):
        book_id = self.kwargs["pk"]
        book = Book.objects.get(pk=book_id)

        review = form.save(commit=False)
        review.book = book
        review.user = self.request.user
        review.save()

        messages.success(self.request, "Your review has been added successfully!")
        return super().form_valid(form)


class ReturnView(FormView):
    template_name = "users/return.html"
    form_class = ReturnForm
    success_url = reverse_lazy("profile")


class UserProfileDetailView(LoginRequiredMixin, DetailView):

    model = User
    template_name = "users/profile.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user


class UserProfileUpdateView(UpdateView):

    model = User
    form_class = UserProfileForm
    template_name = "users/profile_update.html"
    success_url = reverse_lazy("profile_update_success")

    def get_object(self, queryset=None):
        return self.request.user
