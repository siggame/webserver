import os
from django.contrib import messages

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(SETTINGS_DIR)
BUILDOUT_DIR = os.path.dirname(PROJECT_DIR)
VAR_DIR = os.path.join(BUILDOUT_DIR, "var")

##########################################################################
#
# Secret settings
#
##########################################################################
# If a secret_settings file isn't defined, open a new one and save a
# SECRET_KEY in it. Then import it. All passwords and other secret
# settings should be stored in secret_settings.py. NOT in settings.py
try:
    from secret_settings import *
except ImportError:
    print "Couldn't find secret_settings file. Creating a new one."
    secret_settings_loc = os.path.join(SETTINGS_DIR, "secret_settings.py")
    with open(secret_settings_loc, 'w') as secret_settings:
        secret_key = ''.join([chr(ord(x) % 90 + 33) for x in os.urandom(40)])
        secret_settings.write("SECRET_KEY = '''%s'''\n" % secret_key)
    from secret_settings import *

##########################################################################
#
# Administrative settings
#
##########################################################################

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


##########################################################################
#
#  Authentication settings
#
##########################################################################

# When a user successfully logs in, redirect here by default
LOGIN_REDIRECT_URL = '/'

# Require that users who are signing up provide an email address
ACCOUNT_EMAIL_REQUIRED = True

# ACCOUNT_EMAIL_VERIFICATION  is set in development.py and production.py

ACCOUNT_EMAIL_SUBJECT_PREFIX = "[SIG-Game]"

ACCOUNT_AUTHENTICATION_METHOD = "username_email"

# Try to pull username/email from provider.
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': { 'access_type': 'online' }
    },
    'github': {
        'SCOPE': ['user:email'],
    }
}

# Django Guardian settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'allauth.account.auth_backends.AuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
)
ANONYMOUS_USER_ID = -1

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/profile/%s/" % u.username,
}

##########################################################################
#
# API settings
#
##########################################################################

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    )
}


##########################################################################
#
# Bleach settings
#
##########################################################################
import bleach

ALLOWED_HTML_TAGS = bleach.ALLOWED_TAGS + ['h1', 'h2', 'h3', 'p', 'img']

ALLOWED_HTML_ATTRS = bleach.ALLOWED_ATTRIBUTES
ALLOWED_HTML_ATTRS.update({
        'img': ['src', 'alt'],
        })

##########################################################################
#
# Crispy settings
#
##########################################################################

CRISPY_TEMPLATE_PACK = 'bootstrap3'


##########################################################################
#
# Celery settings
#
##########################################################################
import djcelery
djcelery.setup_loader()

try:
    BROKER_URL
except NameError:
    BROKER_URL = 'django://'

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']


##########################################################################
#
# Competition settings
#
##########################################################################

QR_DIR = os.path.join(VAR_DIR, "qr")
COMPETITION_DEFAULT_THUMB = "/static/img/default_competition_image_t.png"


##########################################################################
#
# Greta settings
#
##########################################################################

GRETA_ROOT_DIR = os.path.join(VAR_DIR, "repos")
GRETA_ROOT_TEST_DIR = os.path.join(VAR_DIR, "test_repos")
GRETA_ARCHIVE_DIR = os.path.join(VAR_DIR, "archives")
GRETA_PAGE_COMMITS_BY = 10

##########################################################################
#
# Git settings
#
##########################################################################

# These settings should be included in secret_settings.py

# GIT_HOST = None
# GIT_PORT = None
GIT_PROTOCOL = 'ssh'


##########################################################################
#
# Testing settings
#
##########################################################################

# Sets the testrunner to Nose
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


##########################################################################
#
# Blog settings
#
##########################################################################



##########################################################################
#
# Messages settings
#
##########################################################################

# Change the default messgae tags to play nice with Bootstrap
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


##########################################################################
#
# Connection settings
#
##########################################################################

ALLOWED_HOSTS = ["localhost", "megaminerai.com"]

##########################################################################
#
# Database settings
#
##########################################################################

# Should be overridden by development.py or production.py
DATABASES = None

# Make every HTTP request an atomic transaction
ATOMIC_REQUESTS = True

# Add project/fixtures to the list of places where django looks for
# fixtures to install.
FIXTURE_DIRS = (
    os.path.join(PROJECT_DIR, "fixtures"),
)


##########################################################################
#
# Cache settings
#
##########################################################################

CACHE_MIDDLEWARE_SECONDS = 5
CACHE_MIDDLEWARE_KEY_PREFIX = 'web_cache'

##########################################################################
#
# Location settings
#
##########################################################################

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = True


##########################################################################
#
# Static files settings
#
##########################################################################
MEDIA_ROOT = os.path.join(VAR_DIR, "uploads")
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(VAR_DIR, "static")
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, "static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


##########################################################################
#
# Template settings
#
##########################################################################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        'OPTIONS': {
            'debug': False,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

                # for django-admin-tools
                'django.template.context_processors.request',

            ],
            # List of callables that know how to import templates from various sources.
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
            ],
        },
    },
]

##########################################################################
#
# Middleware settings
#
##########################################################################

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)


##########################################################################
#
# URL settings
#
##########################################################################

ROOT_URLCONF = 'webserver.urls'


##########################################################################
#
# Installed apps settings
#
##########################################################################

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # Django AllAuth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',

    # Django Admin Tools
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    # django-crispy-forms
    'crispy_forms',

    # Competition app
    'competition',

    # Git app
    'greta',

    # API stuff
    'rest_framework',

    'webserver.home',
    'webserver.profiles',
    'webserver.codemanagement',
    'webserver.teammanagement',
    'webserver.hermes',
    'webserver.utility',

    'guardian',
    'djcelery',                 # Django celery
    'kombu.transport.django',
    'raven.contrib.django.raven_compat',  # Sentry client
    'django_extensions',
    'django_nose',
)


##########################################################################
#
# Logging settings
#
##########################################################################

# Check development.py or production.py for specific logging settings.
LOGGING = None
