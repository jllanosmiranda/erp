from django.contrib.auth.models import User
from django.db import models

from core.models import EntityBaseModel


# Create your models here.


class Business(EntityBaseModel):
    singleton = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    website = models.URLField(max_length=200, null=True, unique=True, blank=True)
    ruc = models.CharField(max_length=15, null=True, unique=True, blank=True)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(singleton=True)
        return obj

class PurchaseSettings(EntityBaseModel):
    vat = models.FloatField(default=0)
