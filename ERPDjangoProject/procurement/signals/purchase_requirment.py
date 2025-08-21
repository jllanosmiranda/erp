from procurement.models import PurchaseRequirement, PurchaseRequirementEvent, PurchaseRequirementItems, PurchaseRequirementItemEvent
from procurement.models import SupplierProduct
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import logging

log = logging.getLogger(__name__)

from main.signals import update_event, create_event


@receiver(post_save, sender=PurchaseRequirement)
def create_purchase_requirement_event(sender, instance, created, **kwargs):
    create_event(sender, instance, created, PurchaseRequirementEvent)


@receiver(pre_save, sender=PurchaseRequirement)
def update_purchase_requirement_event(sender, instance, **kwargs):
    update_event(sender, instance, PurchaseRequirementEvent)

@receiver(post_save, sender=PurchaseRequirementItems)
def create_purchase_requirement_item_event(sender, instance, created, **kwargs):
    create_event(sender, instance, created, PurchaseRequirementItemEvent)
    supplier_product = SupplierProduct.objects.get(pk=instance.supplier_product.pk)
    supplier_product._changed_by = instance._changed_by
    if supplier_product.price != instance.price:
        supplier_product.price=instance.price
    if supplier_product.currency != instance.currency:
        supplier_product.currency=instance.currency
    if supplier_product.unit_of_measure != instance.unit_of_measure:
        supplier_product.unit_of_measure=instance.unit_of_measure

    supplier_product.save()



@receiver(pre_save, sender=PurchaseRequirementItems)
def update_purchase_requirement_item_event(sender, instance, **kwargs):
    update_event(sender, instance, PurchaseRequirementItemEvent)

    supplier_product = SupplierProduct.objects.get(pk=instance.supplier_product.pk)
    supplier_product._changed_by = instance._changed_by
    if supplier_product.price != instance.price:
        supplier_product.price = instance.price
    if supplier_product.currency != instance.currency:
        supplier_product.currency = instance.currency
    if supplier_product.unit_of_measure != instance.unit_of_measure:
        supplier_product.unit_of_measure = instance.unit_of_measure

    supplier_product.save()
