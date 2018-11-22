# coding=utf-8
"""
Django settings for zis project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
gettext = lambda s: s

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7cz57t826tnujp*e%#y!jxoe@=f(ogo&@s2=ok^@j2jedcglrw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'zis.localhost',
    'localhost',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # 'django.contrib.sites',

    'loginas',
    'ckeditor',
    'django_extensions',

    'ziscz.web',
    'ziscz.core',
    'ziscz.api',

    'webpack_loader',
    'imagekit',
    'rest_framework',
    'crispy_forms',
    'bootstrap_datepicker_plus',
    'django_select2',
    'colorful',
    'django_js_reverse',
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ziscz.zis.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/


TIME_ZONE = 'Europe/Prague'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ROOT_URLCONF = 'ziscz.zis.urls'

LANGUAGE_CODE = 'cs'

LANGUAGES = (
    ('cs', gettext('Czech')),
    ('en', gettext('English')),
)

LOCALE_PATHS = os.path.join(BASE_DIR, 'locale'),

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ["Format", "Bold", "Italic", "Underline", "Strike", "SpellChecker"],
            ['NumberedList', 'BulletedList', "Indent", "Outdent", 'JustifyLeft', 'JustifyCenter',
             'JustifyRight', 'JustifyBlock'],
            ["Table", "Link", "Unlink", "Anchor", "SectionLink", "Subscript", "Superscript"],
            ['Undo', 'Redo'], ["Source"],
            ["Maximize"]
        ],
        'height': 480,
        'width': 1280,
        'allowedContent': True,
        'removeFormatAttributes': '',
    },
}

LOGINAS_REDIRECT_URL = '/'

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': False,
        'BUNDLE_DIR_NAME': 'build/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

BOOTSTRAP4 = {
    'include_jquery': True,
}

JS_REVERSE_EXCLUDE_NAMESPACES = ['admin']

ICONS_PATH = os.path.join(BASE_DIR, 'web/static/img/icons/animals/')

INTERNAL_IPS = ['127.0.0.1', ]

LOGIN_REDIRECT_URL = '/'

SESSION_COOKIE_AGE = 30 * 60  # 30 minutes
SESSION_SAVE_EVERY_REQUEST = True
