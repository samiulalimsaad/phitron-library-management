from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    AddReviewView,
    BookDetailView,
    BookListView,
    BorrowBookView,
    BorrowSuccessView,
    DepositSuccessView,
    DepositView,
    ReturnBookView,
    UserRegistrationView,
    home,
    profile_view,
)

urlpatterns = [
    path("", home, name="home"),
    path("books/", BookListView.as_view(), name="book_list"),
    # path("books/<int:pk>/borrow/", borrow_book, name="borrow_book"),
    path("books/<int:pk>/borrow/", BorrowBookView.as_view(), name="borrow_book"),
    path("books/<int:pk>/return/", ReturnBookView.as_view(), name="return_book"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("books/<int:pk>/add_review/", AddReviewView.as_view(), name="add_review"),
    # users
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("profile/", profile_view, name="profile"),
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("success_deposit/", DepositSuccessView.as_view(), name="success_deposit"),
    path("success_borrow/", BorrowSuccessView.as_view(), name="success_borrow"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
