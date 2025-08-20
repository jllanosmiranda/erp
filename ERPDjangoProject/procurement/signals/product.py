from ..models.products import ProductEvents, Product
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import logging

log = logging.getLogger(__name__)

@receiver(post_save, sender=Product)
def create_product_events(sender, instance, created, **kwargs):
    if not created:
        return

    event = ProductEvents(product=instance,
                          action=ProductEvents.CREATE,
                          changed_by=instance._changed_by
                          )
    event.save()

@receiver(pre_save, sender=Product)
def update_product_events(sender, instance, **kwargs):
    if not instance.pk:
        return

    old_instance = sender.objects.get(pk=instance.pk)

    for field in instance._meta.fields:
        field_name = field.name
        if field_name == ("updated_at",):
            continue

        old_value = getattr(old_instance, field_name)
        new_value = getattr(instance, field_name)
        if old_value != new_value:
            event = ProductEvents.objects.create(product=instance,
                                                 field_name=field_name,
                                                 old_value=old_value,
                                                 new_value=new_value,
                                                 action=ProductEvents.UPDATE,
                                                 changed_by=instance._changed_by
                                                 )
            event.save()
