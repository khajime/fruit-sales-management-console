from django.db import models
from django.urls import reverse


class Sale(models.Model):
    """販売情報モデル"""
    fruit = models.ForeignKey('fruits.Fruit', null=True, on_delete=models.CASCADE)
    # fruit_name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    sold_at = models.DateTimeField()

    def __str__(self):
        return self.fruit.name

    def get_absolute_url(self):
        return reverse('fruitsale_list')