from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView, UpdateView

from .forms import (
    BorrowForm,
    DepositForm,
    ReturnForm,
    ReviewForm,
    UserProfileForm,
    UserRegistrationForm,
)
from .models import Book


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "books"


class BorrowBookView(LoginRequiredMixin, View):
    template_name = "borrow_book.html"

    def get(self, request, *args, **kwargs):
        book_id = kwargs["pk"]
        book = Book.objects.get(pk=book_id)
        return render(request, self.template_name, {"book": book})

    def post(self, request, *args, **kwargs):
        return redirect("book_list")


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
    template_name = "deposit.html"
    form_class = DepositForm
    success_url = reverse_lazy("deposit_success")


class BorrowView(FormView):
    template_name = "borrow.html"
    form_class = BorrowForm
    success_url = reverse_lazy("borrow_success")


class ReturnView(FormView):
    template_name = "return.html"
    form_class = ReturnForm
    success_url = reverse_lazy("return_success")


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
