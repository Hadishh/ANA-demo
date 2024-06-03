from django.db import models

# Create your models here.
class Conversation(models.Model):
    message = models.CharField()
    answer = models.CharField()
    time = models.DateTimeField(auto_now_add=True)

class Dictionary(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField()