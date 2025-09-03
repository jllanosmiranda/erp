from procurement.models import PurchaseRequirement, PurchaseRequirementEvent, PurchaseRequirementItems, PurchaseRequirementItemEvent
from procurement.models import SupplierProduct
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import logging

log = logging.getLogger(__name__)

from core.signals import create_event, update_event


@receiver(post_save, sender=PurchaseRequirement)
def create_purchase_requirement_event(sender, instance, created, **kwargs):
    create_event(sender, instance, created, PurchaseRequirementEvent)


@receiver(pre_save, sender=PurchaseRequirement)
def update_purchase_requirement_event(sender, instance, **kwargs):
    update_event(sender, instance, PurchaseRequirementEvent)

def update_supplier_base_on_purchase_requirement_item(purchase_requirement_item: PurchaseRequirementItems,):
    supplier_product = SupplierProduct.objects.get(pk=purchase_requirement_item.supplier_product.pk)
    supplier_product._changed_by = purchase_requirement_item._changed_by
    if supplier_product.price != purchase_requirement_item.price:
        supplier_product.price=purchase_requirement_item.price
    if supplier_product.currency != purchase_requirement_item.currency:
        supplier_product.currency=purchase_requirement_item.currency
    if supplier_product.unit_of_measure != purchase_requirement_item.unit_of_measure:
        supplier_product.unit_of_measure=purchase_requirement_item.unit_of_measure

    supplier_product.save()


@receiver(post_save, sender=PurchaseRequirementItems)
def create_purchase_requirement_item_event(sender, instance, created, **kwargs):
    create_event(sender, instance, created, PurchaseRequirementItemEvent)
    update_supplier_base_on_purchase_requirement_item(instance)



@receiver(pre_save, sender=PurchaseRequirementItems)
def update_purchase_requirement_item_event(sender, instance, **kwargs):
    update_event(sender, instance, PurchaseRequirementItemEvent)
    update_supplier_base_on_purchase_requirement_item(instance)

