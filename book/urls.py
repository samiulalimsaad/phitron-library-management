# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    BookDetailView,
    BookListView,
    BorrowBookView,
    ReturnBookView,
    UserProfileView,
)

urlpatterns = [
    path("books/", BookListView.as_view(), name="book_list"),
    path("books/<int:pk>/borrow/", BorrowBookView.as_view(), name="borrow_book"),
    path("books/<int:pk>/return/", ReturnBookView.as_view(), name="return_book"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
