from django.db import models
from django.urls import reverse


class Sale(models.Model):
    """販売情報モデル"""
    fruit = models.ForeignKey('fruits.Fruit', null=True, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(null=True)
    amount = models.PositiveIntegerField(null=True)
    sold_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.fruit.name

    def get_absolute_url(self):
        return reverse('fruitsale_list')
