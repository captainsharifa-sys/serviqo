from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Business(models.Model):

    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    category = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=30
    )

    address = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


    def __str__(self):

        return self.name



class Service(models.Model):

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="services"
    )

    name = models.CharField(
        max_length=200
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    duration = models.PositiveIntegerField(
        help_text="Duration in minutes"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return self.name



class WorkingHour(models.Model):

    DAYS = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]


    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="working_hours"
    )

    day = models.CharField(
        max_length=20,
        choices=DAYS
    )

    open_time = models.TimeField()

    close_time = models.TimeField()

    is_closed = models.BooleanField(
        default=False
    )


    class Meta:

        unique_together = (
            "business",
            "day"
        )


    def __str__(self):

        return f"{self.business.name} - {self.day}"