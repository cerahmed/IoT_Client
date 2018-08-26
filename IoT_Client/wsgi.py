"""
WSGI config for IoT_Client project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from .zeroconf.connectZeroconfService import connectToServer

def onStartup():
    '''
    This function is meant to run on each startup of the server.
    1) connect to local IoT-server zeroconf service.
    '''
    
    connectToServer()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IoT_Client.settings')
onStartup() # This script will run when the server first runs

application = get_wsgi_application()
