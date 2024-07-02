from django.db import models

from chat.models import User


class BookReader(models.Model):

    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    last_book_read = models.TextField()
    chapter = models.PositiveIntegerField()
