from procurement.models import Supplier, SupplierEvent
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import logging

log = logging.getLogger(__name__)

from core.signals import create_event, update_event


@receiver(post_save, sender=Supplier)
def create_supplier_events(sender, instance, created, **kwargs):
    create_event(sender, instance, created, SupplierEvent)


@receiver(pre_save, sender=Supplier)
def update_supplier_events(sender, instance, **kwargs):
    update_event(sender, instance, SupplierEvent)
