# settings_dev.py

from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'open_companies_db',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'db',  # Use the Docker service name
        'PORT': '5432',  # Port inside the container
    }
}

DEBUG = True

ALLOWED_HOSTS = ['*', '0.0.0.0']

