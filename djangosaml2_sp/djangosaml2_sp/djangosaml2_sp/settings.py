"""
Django settings for djangosaml2_sp project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'btl-x0ja09$zqer3h^n^_ic!9h+1q0g!-wqzj&&zio@(@5p*no'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['sp.pysaml2.testunical.it',]

# Application definition

INSTALLED_APPS = [
    # custom user model
    'custom_accounts',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # SAML2 SP
    'djangosaml2',
    'saml2_sp',

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

ROOT_URLCONF = 'djangosaml2_sp.urls'

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

WSGI_APPLICATION = 'djangosaml2_sp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangosaml2_sp',
        'HOST': 'localhost',
        'USER': 'djangosaml2_sp',
        'PASSWORD': 'djangosaml2_sp78',
        'PORT': ''
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

AUTH_USER_MODEL = 'custom_accounts.User'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'


if 'djangosaml2' in INSTALLED_APPS:
    # from . import sp_pysaml2
    from . import sp_pysaml2_shibidp as sp_pysaml2
    
    # pySAML2 SP mandatory
    SESSION_EXPIRE_AT_BROWSER_CLOSE=True
    
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'djangosaml2.backends.Saml2Backend',
    )
    
    LOGIN_URL = '/saml2/login/'
    LOGOUT_URL = '/logout/'
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/'

    BASE_URL = sp_pysaml2.BASE_URL

    # OR NAME_ID or MAIN_ATTRIBUTE (not together!)
    # SAML_USE_NAME_ID_AS_USERNAME = sp_pysaml2.SAML_USE_NAME_ID_AS_USERNAME 

    SAML_DJANGO_USER_MAIN_ATTRIBUTE = sp_pysaml2.SAML_DJANGO_USER_MAIN_ATTRIBUTE
    SAML_DJANGO_USER_MAIN_ATTRIBUTE_LOOKUP = sp_pysaml2.SAML_DJANGO_USER_MAIN_ATTRIBUTE_LOOKUP

    SAML_CREATE_UNKNOWN_USER = sp_pysaml2.SAML_CREATE_UNKNOWN_USER
    SAML_CONFIG = sp_pysaml2.SAML_CONFIG
    SAML_ATTRIBUTE_MAPPING = sp_pysaml2.SAML_ATTRIBUTE_MAPPING
    
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
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
            'djangosaml2': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        }
    }
