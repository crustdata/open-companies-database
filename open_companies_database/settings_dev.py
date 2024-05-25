# settings_dev.py

from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'open_companies_db',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '35432',
    }
}

DEBUG = True

ALLOWED_HOSTS = ['*', '0.0.0.0']

