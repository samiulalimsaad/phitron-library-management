from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ReviewForm
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
        # Handle borrowing logic
        # Update user balance, create borrowing record, etc.
        return redirect("book_list")


class ReturnBookView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Handle returning logic
        return redirect("user_profile")


class UserProfileView(LoginRequiredMixin, View):
    template_name = "user_profile.html"

    def get(self, request, *args, **kwargs):
        # Display user profile, borrowing history, etc.
        return render(request, self.template_name)


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
