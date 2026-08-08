from django.db import models
from dashboard.models import Business, Service


class Customer(models.Model):

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="customers"
    )

    name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=30
    )

    email = models.EmailField(
        blank=True
    )

    favorite_service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="favorite_customers"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Appointment(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
        ("Completed", "Completed"),
    ]

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="appointments",
        null=True,
        blank=True,
    )

    customer_name = models.CharField(
        max_length=100
    )

    customer_phone = models.CharField(
        max_length=30
    )

    customer_email = models.EmailField(
        blank=True
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.customer_name} - {self.service.name}"