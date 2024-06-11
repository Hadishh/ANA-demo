from django.db import models
from users.models import User
class Message(models.Model):

    src_choices = (
        ("bot", "bot"),
        ("user", "user")
    )

    type_choices = (
        ("joke", "joke"),
        ("read book", "read book"),
        ("story", "story"),
        ("phone", "phone"),
        ("other", "other")
    )
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    text = models.TextField(name="text")
    date = models.DateTimeField(auto_now_add=True, name='date')
    source = models.CharField(choices=src_choices, max_length=5)
    type = models.CharField(choices=type_choices, max_length=64, default="other")