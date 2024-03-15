# Generated by Django 5.0 on 2024-03-14 21:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_review_rating_borrowinghistory_useraccount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='borrowinghistory',
            unique_together={('user', 'book')},
        ),
    ]