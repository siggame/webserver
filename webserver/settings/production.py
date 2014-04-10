"""Settings file for project deployment

"""
from webserver.settings.defaults import *

# Choose which site we're using. initial_data.yaml installs some
# fixture data so that localhost:8000 has SIDE_ID == 1, and
# megaminerai.com has SITE_ID == 2
#
# Since we're deploying on megaminerai.com, SITE_ID should be 2.
SITE_ID = 2

# Since we're behind a proxy
USE_X_FORWARDED_HOST = True

# Require that users verify their account before they can login.
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

# Cache flatpages for a minute
FLATPAGE_TIMEOUT = 60

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': POSTGRES_DB,            # Should be in secret_settings.py
        'USER': POSTGRES_USER,          # Should be in secret_settings.py
        'PASSWORD': POSTGRES_PASSWORD,  # Should be in secret_settings.py
        'HOST': 'localhost'
    }
}

CACHES = {
    'default' : {
        'BACKEND':'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [MEMCACHED_LOCATION],   # Should be in secret_settings.py
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry', 'console', 'logfile'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(VAR_DIR, "logs", "log.txt"),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },

        # Log all debug information for our apps to stdout and to a file
        'webserver': {
            'level': 'DEBUG',
            'handlers': ['console', 'logfile'],
            'propagate': True,
        },
        'competition': {
            'level': 'DEBUG',
            'handlers': ['console', 'logfile'],
            'propagate': True,
        }
    }
}
