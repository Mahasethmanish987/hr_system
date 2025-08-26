from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model

class LeaveModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leave_module'

    def ready(self):
        User = get_user_model()

        def create_default_superuser(sender, **kwargs):
            from decouple import config
            from django.db.utils import OperationalError

            try:
                username = config("DJANGO_SUPERUSER_USERNAME", default="admin")
                email = config("DJANGO_SUPERUSER_EMAIL", default="admin@example.com")
                password = config("DJANGO_SUPERUSER_PASSWORD", default="admin123")

                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(username=username, email=email, password=password)
                    print(f"✅ Superuser {username} created.")
            except OperationalError:
                pass  # Ignore if DB isn't ready yet

        # Do NOT use sender=self; use AppConfig class instead
        post_migrate.connect(create_default_superuser, sender=self.__class__)
