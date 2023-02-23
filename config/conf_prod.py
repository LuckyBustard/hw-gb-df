import os

from .settings import *

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "3h5@e047d+nk&0i+afo@6a-o*r*wnicj2e@gqpbno&*(zx4k10")

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "mian",
        "USER": "user",
        "PASSWORD": "pass",
        "HOST": "db",
        "PORT": "5432",
    }
}

del STATICFILES_DIRS
STATIC_ROOT = BASE_DIR / "static"
