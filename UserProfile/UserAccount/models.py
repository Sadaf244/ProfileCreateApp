from django.db import models
from django.contrib.auth.models import AbstractUser


    
class UserModel(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    password = models.CharField(max_length=150, null=False, blank=False)
    bio = models.CharField(max_length=150, null=True, blank=True)
    file_upload = models.ImageField(upload_to='userdocs', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email