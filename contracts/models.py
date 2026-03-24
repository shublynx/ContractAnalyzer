import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email' # Log in with email
    REQUIRED_FIELDS = ['username'] # Username still required by Django internally


class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contracts')
    file = models.FileField(upload_to='contracts/%Y/%m/%d/')
    name = models.CharField(max_length=255)
    raw_text = models.TextField(blank=True, null=True) # Where the extracted PDF text lives
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.email}"