from ..models.supplier_product import SupplierProduct, SupplierProductEvent
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import logging

log = logging.getLogger(__name__)

from main.signals import update_event, create_event


@receiver(post_save, sender=SupplierProduct)
def create_supplier_product_events(sender, instance, created, **kwargs):
    create_event(sender, instance, created, SupplierProductEvent)


@receiver(pre_save, sender=SupplierProduct)
def update_supplier_product_events(sender, instance, **kwargs):
    update_event(sender, instance, SupplierProductEvent)
