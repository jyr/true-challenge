from os import environ

from .base import *

ALLOWED_HOSTS = ['.execute-api.us-east-2.amazonaws.com']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': environ['NAME_DB'],
        'USER': environ['USER_DB'],
        'PASSWORD': environ['PASSWORD_DB'],
        'HOST': environ['HOST_DB'],
        'PORT': environ['PORT_DB']
    }
}

GDAL_LIBRARY_PATH = "/opt/lib/libgdal.so.20.1.3"
GEOS_LIBRARY_PATH = "/opt/lib/libgeos_c.so.1"
