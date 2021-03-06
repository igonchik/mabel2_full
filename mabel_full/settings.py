import os

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'f!l9nm*66y#bezuw)7(x5o=9-=-w@zpczgmi!2i$3q^dpmo+4c'
KEY = 'egsdasddaasgfbxbvbvc3423r23%%$Fv'

ADMINS = [
    ("Dmitry", "igonchik@gmail.com"),
]
MANAGERS = ADMINS
ALLOWED_HOSTS = [
    '127.0.0.1',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mebel_full',
        'USER': 'postgres',
    }
}

CSRF_COOKIE_NAME = 'bro'
CSRF_COOKIE_AGE = 86400
CSRF_FAILURE_VIEW = 'mabel_full.errhandlers.csrf_failure'
ugettext = lambda s: s
LANGUAGES = (
    ('en', ugettext('English')),
    ('ru', ugettext('Russian')),
)

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru_RU.utf8'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False

INSTALLED_APPS = [
    'mebel2.apps.Mebel2Config',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, '_locale/'),
)
LANGUAGE_COOKIE_NAME = 'curlang'

DATETIME_INPUT_FORMATS = (
    '%d.%m.%Y %H:%M',
    '%d.%m.%Y %H:%M:%S',
    '%d.%m.%Y',
)

DATE_INPUT_FORMATS = (
    '%d.%m.%Y',
    '%d.%m.%Y %H:%M',
    '%d.%m.%Y %H:%M:%S',
)

TIME_INPUT_FORMATS = (
    '%H:%M:%S',
    '%H:%M',
)

X_FRAME_OPTIONS = 'DENY'
ROOT_URLCONF = 'mabel_full.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'mabel_full.config.globs',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_ROOT = os.path.join(BASE_DIR, '_medialib')
MEDIA_URL = '/medialib/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '_static'),
)

WSGI_APPLICATION = 'mabel_full.wsgi.application'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#EMAIL_HOST = '110.1.1.242'
#EMAIL_PORT = '25'
#SERVER_EMAIL = 'special-admin@mss.fso'
