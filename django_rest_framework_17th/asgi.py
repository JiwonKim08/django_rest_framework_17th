

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_framework_17th.settings')

application = get_asgi_application()
