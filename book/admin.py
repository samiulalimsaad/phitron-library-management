from django.contrib import admin

from book.models import Book, BorrowingHistory, Category, Review, UserAccount

# Register your models here.

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(UserAccount)
admin.site.register(BorrowingHistory)
