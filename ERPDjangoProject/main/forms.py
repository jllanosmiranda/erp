from django.forms.models import ModelForm
from main.models import Business


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'address', 'phone', 'email', 'website', 'ruc']
