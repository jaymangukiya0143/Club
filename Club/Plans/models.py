from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


class Plans(models.Model):
    name = models.CharField(max_length=30,default="")
    description = models.TextField(default='')
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)],default='12')
    fees = models.DecimalField(max_digits=8,decimal_places=2,default=0.00)

    def __str__(self):
        return self.name