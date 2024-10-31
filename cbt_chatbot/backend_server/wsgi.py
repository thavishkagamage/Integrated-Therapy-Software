"""
This file is responsible for configuring the Web Server Gateway Interface (WSGI) for the backend_server project.
WSGI is a specification that defines how web servers communicate with web applications in Python.
This file is essential for deploying your Django application on a production server.

Key Points:
1. WSGI Configuration:
   - The file sets up the WSGI configuration for the Django project, making it possible to serve the application using a WSGI-compatible web server.

2. Environment Variable:
   - It sets the DJANGO_SETTINGS_MODULE environment variable to 'backend_server.settings', which tells Django to use the settings from the backend_server/settings.py file.

3. WSGI Application:
   - It exposes the WSGI callable as a module-level variable named application. This callable is used by WSGI servers to forward requests to the Django application.

Code Breakdown:
- Imports:
  - os: Provides a way to interact with the operating system.
  - get_wsgi_application: A Django function that returns the WSGI application callable.

- Environment Variable:
  - os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_server.settings'): Sets the default settings module for the Django project.

- WSGI Application:
  - application = get_wsgi_application(): Retrieves the WSGI application callable, which is used by WSGI servers to handle requests.

Usage:
- Development:
  - In development, the Django development server uses this configuration to serve the application.

- Production:
  - In production, a WSGI server like Gunicorn or uWSGI uses this configuration to serve the application.

For more information, you can refer to the Django documentation on WSGI: https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_server.settings')

application = get_wsgi_application()
