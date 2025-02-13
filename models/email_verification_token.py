from django.db import models
from django.utils import timezone
from datetime import timedelta
from .user_model import User
import uuid


class EmailVerificationToken(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification_token')
  token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  created_at = models.DateTimeField(auto_now=True)
  expires_at = models.DateTimeField()
  
  def save(self, *args, **kwargs):
    if not self.expires_at:
      self.expires_at = timezone.now() + timedelta(minutes=30)
    super().save(*args,**kwargs)
    
  def is_expired(self):
    return timezone.now() > self.expires_at