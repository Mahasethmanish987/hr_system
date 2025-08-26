"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()


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
