from django.db import models
from django.contrib.auth.models import User


class Business(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)

    category = models.CharField(max_length=100)

    phone = models.CharField(max_length=30)

    address = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
class Service(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="services"
    )

    name = models.CharField(max_length=200)

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    duration = models.PositiveIntegerField(
        help_text="Duration in minutes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name
    