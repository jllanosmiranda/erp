from ..models.supplier_product import SupplierProduct, SupplierProductEvent
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import logging

log = logging.getLogger(__name__)

@receiver(post_save, sender=SupplierProduct)
def create_supplier_product_events(sender, instance, created, **kwargs):
    if not created:
        return

    event = SupplierProductEvent(supplier_product=instance,
                                 action=SupplierProductEvent.CREATE,
                                 changed_by=instance._changed_by
                                )
    event.save()

@receiver(pre_save, sender=SupplierProduct)
def update_supplier_product_events(sender, instance, **kwargs):
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
            event = SupplierProductEvent.objects.create(supplier_product=instance,
                                                        field_name=field_name,
                                                        old_value=old_value,
                                                        new_value=new_value,
                                                        action=SupplierProductEvent.UPDATE,
                                                        changed_by=instance._changed_by
                                                        )
            event.save()
