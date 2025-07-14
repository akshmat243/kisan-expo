from django.apps import AppConfig


class EcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ECommerce'
    
    def ready(self):
        import ECommerce.signals
