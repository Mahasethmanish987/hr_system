from django.apps import AppConfig


class EmployeeModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employee_module'

    def ready(self): 
        import employee_module.signals 
