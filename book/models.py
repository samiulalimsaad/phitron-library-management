from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="book_images/")
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2)
    reviews = models.ManyToManyField(User, through="Review")
    categories = models.ManyToManyField(Category)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
