from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('CITIZEN', 'Citizen'),
        ('WORKER', 'Municipal Worker'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CITIZEN')
    id_card_number = models.CharField(max_length=50, blank=True, null=True)
    photo_verification = models.ImageField(upload_to='worker_photos/', blank=True, null=True)
