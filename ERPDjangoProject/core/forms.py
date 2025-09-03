from django.forms.models import ModelForm
import logging
log = logging.getLogger(__name__)



class EntityBaseModelForm(ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit = True):
        model_object = super().save(commit=False)
        if not model_object.pk:
            model_object.created_by = self.user
        model_object.updated_by = self.user

        if commit:
            model_object.save()
            return model_object

        return model_object
