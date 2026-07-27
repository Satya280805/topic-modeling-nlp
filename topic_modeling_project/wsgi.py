"""
topic_modeling_project/wsgi.py

WSGI = Web Server Gateway Interface.
This file is the entry point for WSGI-compatible web servers (like Gunicorn)
to serve the Django application in production.
"""

import os
from django.core.wsgi import get_wsgi_application

# Tell Django which settings module to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'topic_modeling_project.settings')

# get_wsgi_application() initializes Django and returns a callable
# that the WSGI server calls for each incoming HTTP request.
application = get_wsgi_application()
