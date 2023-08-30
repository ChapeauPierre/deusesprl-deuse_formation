"""
Django settings for project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os

from datetime import timedelta


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5t2%9ayb*wgh#q)8olz*(dmselm=g1ixec=io1s=#wqv6kw#7%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'false') == 'true'

ADMINS = (
    ('Julien Deuse', 'j.deuse@deuse.be'),
    ('Maxime Deuse', 'm.deuse@deuse.be'),
)


# on DEBUG, allow every host
if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = [
        'deuse-formation.deuse.live',
        'prod.deuse-formation.com',
        'deuse-formation.com',
        'www.deuse-formation.com',
    ]


# Application definition

INSTALLED_APPS = [
    'main',
    'user',
    'topics',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
    'widget_tweaks',
    'webpack_loader',
    'debug_toolbar',
    'maintenance_mode',

    'cms',
    'celery',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
    'cms.middleware.CmsMiddleware',
]

ROOT_URLCONF = 'deuse_formation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'deuse_formation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_SERVICE'),
        'PORT': os.environ.get('DB_PORT')
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fr-BE'

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Django logger <- logs information in the log files
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'file_d': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/debug.log',
            'formatter': 'simple',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
        },
        'file_w': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/warning.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
        },
        'file_elastic': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/elastic.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
        },
        'file_stripe': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/stripe.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
        },
        'console': {   # Logs all WARNINGs in the console
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_d', 'file_w', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'elastic': {
            'handlers': ['file_elastic'],
            'level': 'INFO',
            'propagate': True,
        },
        'stripe': {
            'handlers': ['file_stripe'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# User substitution - We use our own user model
# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#auth-custom-user
AUTH_USER_MODEL = 'user.User'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Media files
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# If this isn't given or is ``None``, you'll get operating-system
# dependent behavior. On most platforms, temporary files will have a mode
# of ``0600``, and files saved from memory will be saved using the
# system's standard umask.
# NB: In Python 3 octal numbers must start with 0o so the line would be:
# Python 2.* => FILE_UPLOAD_PERMISSIONS = 0644
# Python 3.* => FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_PERMISSIONS = 0o644


# Django Rest Framework and Simple JWT
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ] if DEBUG else ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=28),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ['Bearer', 'JWT'],
}


# Django webpack bundle loader
WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'frontend/webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
        'LOADER_CLASS': 'webpack_loader.loader.WebpackLoader',
    }
}

# Celery
CELERY_BROKER_URL = "redis://:{password}@{host}:{port}/{db}".format(
    password=os.environ.get('REDISCLI_AUTH'),
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    db=os.environ.get('CELERY_REDIS_DB')
)
CELERY_RESULT_BACKEND = "redis://:{password}@{host}:{port}/{db}".format(
    password=os.environ.get('REDISCLI_AUTH'),
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    db=os.environ.get('CELERY_REDIS_DB')
)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Django site ID
SITE_ID = 1


# Django Emails
EMAIL_BACKEND = 'deuse_formation.mail.CustomEmailBackend'
DEBUG_EMAIL = os.environ.get('DEBUG_EMAIL')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True


# Django debug toolbar
def show_toolbar(request):
    return bool(DEBUG)


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

# Default Primary Key type
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
