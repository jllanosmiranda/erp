from procurement.models import PurchaseRequirement, PurchaseRequirementEvent
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
