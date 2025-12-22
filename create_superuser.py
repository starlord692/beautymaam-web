import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin_test').exists():
    User.objects.create_superuser('admin_test', 'admin@example.com', 'password123')
    print("Superuser 'admin_test' created.")
else:
    print("Superuser 'admin_test' already exists.")
