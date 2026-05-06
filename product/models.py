from django.db import models

# Create your models here.

class Product(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock  = models.IntegerField(default=10)
    category = models.CharField(max_length=100)

    media = models.ImageField(upload_to='images/')

    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='active')
    



