from django.apps import AppConfig


class ProcurementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'procurement'

    def ready(self):
        import procurement.signals.product
        import procurement.signals.supplier_product
        import procurement.signals.supplier
        import procurement.signals.purchase_requirment
