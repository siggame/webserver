"""Settings file for project development.

These settings should **NOT** be used to deploy
"""
import project.settings.defaults as default_settings
from project.settings.defaults import *

# Choose which site we're using. initial_data.yaml installs some
# fixture data so that localhost:8000 has SIDE_ID == 1, and
# megaminerai.com has SITE_ID == 2
#
# Since we're debugging, we want to keep the site at #1
SITE_ID = 1

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(VAR_DIR, "db", "webserver.db"),
    }
}

MIDDLEWARE_CLASSES = default_settings.MIDDLEWARE_CLASSES + (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS = default_settings.INSTALLED_APPS + (
    'debug_toolbar',
)
