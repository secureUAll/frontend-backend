"""
Django settings for secureuall project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w3f=c#)&_9c3ym!@8ex^dq^+!5*l@z9h)9=$yqd+f6hnd=u=&j'

# SECURITY WARNING: don't run with debug turned on in production!
RUNNING_MODE = os.environ.get("RUNNING_MODE", None)
PRODUCTION = RUNNING_MODE is  not  None  and RUNNING_MODE.lower() == 'production'
DEBUG = not PRODUCTION
# Docker debug allows for local authentication but with connection to the database
DOCKER_DEBUG = RUNNING_MODE is  not  None  and RUNNING_MODE.lower() == 'docker'
print("Prod?", PRODUCTION)
LOGIN_URL = "/login/"

if PRODUCTION or DOCKER_DEBUG:
    # Update configs as you wish
    if not DOCKER_DEBUG:
        print("REST API running in production environment with local authentication.")
        ALLOWED_HOSTS = ['*']
        CORS_ALLOW_ALL_ORIGINS = True
        SECURE_SSL_REDIRECT = False
    else:
        print("REST API running in production environment with UA IdP authentication.")
    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get("DB_NAME", 'postgres'),
            'USER': os.environ.get("DB_USER", 'postgres'),
            'PASSWORD': os.environ.get("DB_PASSWORD", 'postgres'),
            'HOST': os.environ.get("DB_HOST", 'db'),
            'PORT': os.environ.get("DB_PORT", 5432),
        }
    }
else:
    print("REST API running in development environment with local authentication.")
    CORS_ALLOW_ALL_ORIGINS = True
    ALLOWED_HOSTS = ['*']
    SECURE_SSL_REDIRECT = False
    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # UA IdP
    'djangosaml2',
    'django_extensions',
    'corsheaders',
    # Our apps
    'login',
    'dashboard',
    'workers',
    'machines',
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

ROOT_URLCONF = 'secureuall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'secureuall.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------
# |  AUTHORIZATION  |
# -------------------
# AUTH_USER_MODEL = 'django.contrib.auth.models.User'

AUTHENTICATION_BACKENDS = [
    # 'user_aut.backends.CustomUserAuth',
    'django.contrib.auth.backends.ModelBackend', #idp
    'djangosaml2.backends.Saml2Backend', #idp
]

MIDDLEWARE.append('djangosaml2.middleware.SamlSessionMiddleware')
SAML_SESSION_COOKIE_NAME = 'saml_session'

from login.sp_pysaml2 import *