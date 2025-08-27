from django.db import models

from apps import serializers


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    telegram_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Hikvision(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    devise_id = models.CharField(max_length=100)

    def __str__(self):
        return self.company.name
