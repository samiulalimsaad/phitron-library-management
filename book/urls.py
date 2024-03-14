# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    BookDetailView,
    BookListView,
    BorrowBookView,
    BorrowView,
    DepositView,
    ReturnBookView,
    ReturnView,
    UserProfileDetailView,
    UserRegistrationView,
    home,
)

urlpatterns = [
    path("", home, name="home"),
    path("books/", BookListView.as_view(), name="book_list"),
    path("books/<int:pk>/borrow/", BorrowBookView.as_view(), name="borrow_book"),
    path("books/<int:pk>/return/", ReturnBookView.as_view(), name="return_book"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    # users
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("profile/", UserProfileDetailView.as_view(), name="profile"),
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("borrow/", BorrowView.as_view(), name="borrow"),
    path("return/", ReturnView.as_view(), name="return"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
