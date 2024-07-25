# your_app/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


class Drone(models.Model):
    DRONE_MODELS = [
        ('Air 3', 'Air 3'),
        ('Inspire 3', 'Inspire 3'),
        ('Mavic 3 Classic', 'Mavic 3 Classic'),
        ('Mavic 3 Pro', 'Mavic 3 Pro'),
        ('Mini 2 SE', 'Mini 2 SE'),
        ('Mini 3', 'Mini 3'),
        ('Mini 3 Pro', 'Mini 3 Pro'),
        ('Mini 4 Pro', 'Mini 4 Pro'),
    ]

    STATUS_CHOICES = [
        ('online', '在线'),
        ('offline', '离线'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    drone_model = models.CharField(max_length=50, choices=DRONE_MODELS)
    drone_sn = models.CharField(max_length=50, unique=True)
    remote_sn = models.CharField(max_length=50)
    workspace_id = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.drone_sn
