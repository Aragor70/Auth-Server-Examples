from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  
  email = models.CharField(max_length=50, unique=True)
  image = models.CharField(max_length=300, blank=True, default='')
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.email}'