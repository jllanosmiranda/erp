from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EntityBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class EventBaseModel(models.Model):
    CREATE = 1
    UPDATE = 2
    DELETE = 3
    CHOICES = (
        (CREATE, "Created"),
        (UPDATE, "Updated"),
        (DELETE, "Deleted"),
    )
    field_name = models.CharField(max_length=100)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    old_value = models.TextField(null=True)
    new_value = models.TextField(null=True)
    action = models.IntegerField(choices=CHOICES)

    class Meta:
        abstract = True
