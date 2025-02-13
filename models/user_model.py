from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
  email = models.EmailField(unique=True)
  deleted_at = models.DateTimeField(blank=True, null=True)
  last_edited = models.DateTimeField(auto_now=True)

  def soft_delete(self):    
    self.deleted_at = timezone.now()
    self.is_active = False
    self.save()

  def restore(self):    
    self.deleted_at = None
    self.is_active = True
    self.save()