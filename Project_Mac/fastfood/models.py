from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    DRINK = 'DRNK'
    BURGER = 'BRGR'
    SNACK = 'SNCK'
    DESSERT = 'DSRT'

    TYPE_CHOICES = [
        (DRINK, 'Drink'),
        (BURGER, 'Burger'),
        (SNACK, 'Snack'),
        (DESSERT, 'Dessert'),
   ]
    type = models.CharField(max_length=5, choices=TYPE_CHOICES, default=BURGER)
    name = models.CharField(max_length=255, unique=True)
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)],)
    description = models.TextField()

    def __str__(self):
        return f'Product #{self.pk} - Name: {self.name}'
    
    def get_absolute_url(self):
        return f'/product/{self.id}'
