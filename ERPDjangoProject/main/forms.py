from django.forms.models import ModelForm
from main.models import Business, PurchaseSettings
from core.forms import EntityBaseModelForm


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'address', 'phone', 'email', 'website', 'ruc']

class PurchaseSettingsForm(EntityBaseModelForm):

    class Meta:
        model = PurchaseSettings
        fields = ['vat']
