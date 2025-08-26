from django.apps import AppConfig
from django.db.models.signals import post_migrate
def create_default_superuser():
     from decouple import config
     from django.contrib.auth import get_user_model
     from django.db.utils import OperationalError
     
     User = get_user_model()
     
     try:
         username = config("DJANGO_SUPERUSER_USERNAME", default="admin")
         email = config("DJANGO_SUPERUSER_EMAIL", default="admin@example.com")
         password = config("DJANGO_SUPERUSER_PASSWORD", default="admin123")
     
         if not User.objects.filter(username=username).exists():
             User.objects.create_superuser(username=username, email=email, password=password)
             print(f"✅ Superuser {username} created.")
     except OperationalError:
         # Happens during migrations before DB is ready → ignore
         pass

class LeaveModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leave_module'


    def ready(self):
        post_migrate.connect(create_default_superuser, sender=self)
          
