from ..models.products import ProductEvents, Product
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import logging
from main.signals import update_event, create_event

log = logging.getLogger(__name__)

@receiver(post_save, sender=Product)
def create_product_events(sender, instance, created, **kwargs):
    create_event(sender, instance, created, ProductEvents)

@receiver(pre_save, sender=Product)
def update_product_events(sender, instance, **kwargs):
    update_event(sender, instance, ProductEvents)
