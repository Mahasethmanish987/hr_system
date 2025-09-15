from django.apps import AppConfig


class PayrollModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payroll_module'

    def ready(self): 
        import payroll_module.signals 

