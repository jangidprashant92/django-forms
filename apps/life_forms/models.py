from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Test(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("completed", "Completed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.CharField(max_length=100, blank=True, null=True)
    product_type = models.CharField(max_length=50)

    quote_num = models.CharField(max_length=50, blank=True, null=True)
    customer_name = models.CharField(max_length=100, blank=True, null=True)

    details = models.JSONField(default=dict)

    current_step = models.CharField(max_length=50, default="details")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
