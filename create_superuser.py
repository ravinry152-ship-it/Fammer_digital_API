# create_superuser.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmer_digital.settings')
django.setup()

from django.contrib.auth.models import User
from decouple import config

username = config('ADMIN_USERNAME', default='admin')
email    = config('ADMIN_EMAIL', default='admin@example.com')
password = config('ADMIN_PASSWORD', default='admin1234')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser '{username}' created!")
else:
    print(f"ℹ️ Superuser '{username}' already exists.")