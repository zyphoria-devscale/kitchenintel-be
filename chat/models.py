from django.db import models


# Create your models here.
class Conversation(models.Model):
    session_id = models.CharField(max_length=100)
    message = models.TextField()
    role = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
