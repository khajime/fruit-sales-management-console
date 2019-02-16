from django.db import models
from django.urls import reverse


class Fruit(models.Model):
    """果物マスタモデル"""
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('fruit_list')