from django.db import models


# Create your models here.
class Category(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
