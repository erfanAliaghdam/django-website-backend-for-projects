"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""


from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]
# Application definition

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'private_storage',
    'admin_searchable_dropdown',
    'django_filters',
    'corsheaders',
    'rest_framework',
    'smsServices',
    'djoser',
    'debug_toolbar',
    'core',
    'web',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES =  {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.getenv('NAME'),
        'USER':     os.getenv('USER'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST':     os.getenv('HOST'),
        'PORT':     os.getenv('PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core.User'


REST_FRAMEWORK={
    'COERCE_DECIMAL_TO_STRING' : False,
    'PAGE_SIZE' : 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}


DJOSER = {
    'LOGIN_FIELD': 'email',
    "USERNAME_FIELD": "phone",
    'SERIALIZERS':{
        'user_create'  : 'core.api.serializers.UserCreateSerializer',
        'current_user' : 'core.api.serializers.UserSerializer',
        'user_delete': ['rest_framework.permissions.IsAdminUser'],
        'set_phone'  : ['rest_framework.permissions.IsAdminUser'],
        'set_email'  : ['rest_framework.permissions.IsAdminUser'],
        'reset_password' : ['rest_framework.permissions.IsAdminUser'],
        'activation' : ['rest_framework.permissions.IsAdminUser'],
        'set_password' : ['rest_framework.permissions.IsAdminUser'],
    },
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
}



#! TODO : DELETE ON DEV
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]


PRIVATE_STORAGE_ROOT = os.path.join(BASE_DIR, 'private-media')
PRIVATE_STORAGE_AUTH_FUNCTION = 'private_storage.permissions.allow_staff'




ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False

BROKER_URL = 'redis://localhost:6379/2'
CELERY_BROKER_URL = 'redis://localhost:6379/2'
# CELERY_BEAT_SCHEDULE={
#     'notify_customers':{
#         'task':'core.tasks.notify_customers',
#         'schedule': crontab(minute=1),
#         'args':['hello world'],
#     }
# }


EXPIRE_CODE_AFTER_MINUTES = 3