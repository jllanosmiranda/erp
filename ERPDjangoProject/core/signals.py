from core.models import EventBaseModel
import logging
log = logging.getLogger(__name__)


def create_event(sender, instance, created, event_model: type[EventBaseModel], **kwargs):
    if not created:
        return

    event = event_model(instance=instance,
                        action=event_model.CREATE,
                        changed_by=instance.created_by)
    event.save()


def update_event(sender, instance, event_model: type[EventBaseModel], **kwargs):
    if not instance.pk:
        return

    old_instance = sender.objects.get(pk=instance.pk)
    log.info(old_instance)

    for field in instance._meta.fields:
        field_name = field.name
        log.info(field_name)
        if field_name == "updated_at":
            continue

        if field_name == "created_at":
            continue

        if field_name == "created_by":
            continue

        if field_name == "id":
            continue

        if field_name == "updated_by":
            continue

        old_value = getattr(old_instance, field_name)
        new_value = getattr(instance, field_name)
        if old_value == new_value:
            continue
        event = event_model.objects.create(instance=instance,
                                           field_name=field_name,
                                           old_value=old_value,
                                           new_value=new_value,
                                           action=event_model.UPDATE,
                                           changed_by=instance.updated_by)
        event.save()
