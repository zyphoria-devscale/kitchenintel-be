from django.db import models
from shared.utils import generate_id

# Create your models here.
class Conversation(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default=generate_id)
    session_id = models.CharField(max_length=100)
    message = models.TextField()
    role = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
