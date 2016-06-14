"""
Django settings for paws nyc project.
"""
import os

from configurations import Configuration, values
from logging.handlers import SysLogHandler
import warnings

class Common(Configuration):

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    SECRET_KEY = values.SecretValue()

    DEBUG = True
    THUMBNAIL_DEBUG = DEBUG

    ALLOWED_HOSTS = values.ListValue([''], separator=';')

    ADMINS = (('Philip Kalinsky', 'philip.kalinsky@eloquentbits.com'), )

    DATE_FORMAT = '%m/%d/%Y'

    EMAIL = values.EmailURLValue('console://')
    DEFAULT_FROM_EMAIL = 'noreply@pawsnyc.org'
    NOREPLY_EMAIL = 'noreply@pawsnyc.org'

    INTERNAL_IPS = ('127.0.0.1',)

    MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
    SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
    SESSION_STORAGE = 'django.contrib.sessions.backends.cache'

    #SESSION_ENGINE = 'redis_sessions.session'

    # Application definition

    INSTALLED_APPS = (
        'charityadmin.apps.longerusername',
        'django.contrib.contenttypes',
        'grappelli.dashboard',
        'grappelli',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.humanize',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',

        'charityadmin.apps.paws',
        'charityadmin.apps.timeslots',

        'django_extensions',
    )

    MIDDLEWARE_CLASSES = (
        'django.middleware.cache.UpdateCacheMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.gzip.GZipMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.cache.FetchFromCacheMiddleware',
    )

    ROOT_URLCONF = 'charityadmin.apps.paws.urls'

    WSGI_APPLICATION = 'charityadmin.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases
    # http://django-configurations.readthedocs.org/en/latest/values/#configurations.values.DatabaseURLValue
    DATABASES = values.DatabaseURLValue()

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    SITE_ID = 1

    # Localization
    LANGUAGE_CODE = 'en'
    LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'charityadmin', 'locale'),
    )
    ugettext = lambda s: s

    LANGUAGES = (
        ('en', ugettext('English')),
    )

    USE_I18N = True
    USE_L10N = True
    TIME_ZONE = 'America/New_York'
    USE_TZ = True

    #RAVEN_CONFIG = {'dsn': os.environ.get('SENTRY_RAVEN_DSN', ''),}

    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.9/howto/static-files/

    STATIC_ROOT = os.path.join(BASE_DIR, 'charityadmin', 'static')

    STATIC_URL = '/static/'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'charityadmin', 'templates'),],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.messages.context_processors.messages',
                    'django.contrib.auth.context_processors.auth',
                    'django.core.context_processors.debug',
                    'django.core.context_processors.i18n',
                    'django.core.context_processors.media',
                    'django.core.context_processors.static',
                    'django.core.context_processors.request',
                ],
                #'loaders': [
                #    'django.template.loaders.cached.Loader', (
                #        'django.template.loaders.filesystem.Loader',
                #        'django.template.loaders.app_directories.Loader',
                #    ),
                #],
            },
        },
    ]
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }}

    #django-grappelli
    GRAPPELLI_INDEX_DASHBOARD = 'charityadmin.dashboard.CustomIndexDashboard'
    GRAPPELLI_ADMIN_TITLE = "PAWS NYC CMS"

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'syslog': {
                'class': 'logging.handlers.SysLogHandler',
                'facility': SysLogHandler.LOG_LOCAL7,
                'address': '/dev/log',
                'formatter': 'standard',
            },
            'stderr': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
            #'mail_admins': {
            #    'level': 'ERROR',
            #    'class': 'django.utils.log.AdminEmailHandler',
            #    'include_html': False,
            #},
            'request_handler': {
                'class': 'logging.NullHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['syslog', 'stderr'],
                'level': 'DEBUG',
                'propagate': True
            },
            'django.request': {
                'handlers': ['stderr'],
                'level': 'ERROR',
                'propagate': True,
            },
            'django.db.backends': { # Stop SQL debug from logging to main logger
                'handlers': ['request_handler'],
                'level': 'DEBUG',
                'propagate': False
            },
        }
    }


class Dev(Common):
    """
    The in-development settings and the default configuration.
    """

    # this setting is useful for debugging but it will break the admin.
    # You have been warned.
    #TEMPLATE_STRING_IF_INVALID = 'undefined variable [%s]'

    THUMBNAIL_DEBUG = False

    DATABASES = values.DatabaseURLValue()
    Common.INSTALLED_APPS += ('debug_toolbar', )
    Common.MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        #'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        #'debug_toolbar.panels.cache.CachePanel',
        #'debug_toolbar.panels.signals.SignalsPanel',
        #'debug_toolbar.panels.logging.LoggingPanel',
        #'debug_toolbar.panels.redirects.RedirectsPanel',
    ]
    SHELL_PLUS_PRE_IMPORTS = (
        #('module.submodule1', ('class1', 'function2')),
        #('module.submodule2', 'function3'),
        #('module.submodule3', '*'),
        #'module.submodule4'
        ('django.db', 'connection'),
        ('django.db', 'reset_queries'),
    )

class Qa(Common):

    """
    The qa settings and the default configuration.
    """

    DEBUG = False
    THUMBNAIL_DEBUG = False
    EMAIL = values.EmailURLValue('smtp://localhost:25')


class Prod(Common):
    """
    The in-production settings.
    """
    DEBUG = False
    THUMBNAIL_DEBUG = False

    EMAIL = values.EmailURLValue('smtp://localhost:25')
