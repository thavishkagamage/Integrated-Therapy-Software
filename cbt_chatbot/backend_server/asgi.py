"""
ASGI config for backend_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/

This file is responsible for configuring the Asynchronous Server Gateway Interface (ASGI) for the backend_server project.
ASGI is a specification that defines how web servers communicate with web applications in Python, particularly for handling asynchronous web applications.
This file is essential for deploying your Django application on an ASGI-compatible server.

Key Points:

1. ASGI Configuration:
   - The file sets up the ASGI configuration for the Django project, making it possible to serve the application using an ASGI-compatible web server.

2. Environment Variable:
   - It sets the DJANGO_SETTINGS_MODULE environment variable to 'backend_server.settings', which tells Django to use the settings from the backend_server/settings.py file.

3. ASGI Application:
   - It exposes the ASGI callable as a module-level variable named application. This callable is used by ASGI servers to forward requests to the Django application.

Code Breakdown:

- Imports:
  - os: Provides a way to interact with the operating system.
  - get_asgi_application: A Django function that returns the ASGI application callable.

- Environment Variable:
  - os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_server.settings'): Sets the default settings module for the Django project.

- ASGI Application:
  - application = get_asgi_application(): Retrieves the ASGI application callable, which is used by ASGI servers to handle requests.

Usage:

- Development:
  - In development, the Django development server uses this configuration to serve the application.

- Production:
  - In production, an ASGI server like Daphne or Uvicorn uses this configuration to serve the application.

For more information, you can refer to the Django documentation on ASGI: https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_server.settings')

application = get_asgi_application()
