from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Luis Montiel', 'luismmontielg@gmail.com'),
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "books",
        "USER": get_env_variable("DB_USERNAME"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
        "HOST": "",
        "PORT": "",
    }
}

INSTALLED_APPS += ("debug_toolbar",)
INTERNAL_IPS = ("127.0.0.1",)
MIDDLEWARE_CLASSES += \
    ("debug_toolbar.middleware.DebugToolbarMiddleware", )

DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}
