"""
WSGI config for fitbiting project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/sudeepsanyal/webapps/fitbiting/fitbiting')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fitbiting.settings")

application = get_wsgi_application()
