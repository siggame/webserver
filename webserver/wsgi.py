"""
Production WSGI config

It exposes the WSGI callable as a module-level variable named ``application``

Use it with gunicorn or whatever
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings.production")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
