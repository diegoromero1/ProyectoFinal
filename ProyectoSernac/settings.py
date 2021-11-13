"""
Django settings for ProyectoSernac project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z9@gf9%asz0xmvp4sdkqs#5+8!w6sx8t$_@q(a(+^!tv^3ny!q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

ALLOWED_HOSTS = ['proyectosernac.herokuapp.com', '127.0.0.1', 'localhost','*']
# CK EXTENDIDO
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',

    },
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ProyectoSernacApp',
    'ckeditor',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'ProyectoSernac.urls'

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

WSGI_APPLICATION = 'ProyectoSernac.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wk4s1e8bc7ibz6se',
        'USER': 'xzui3qqyza7v4mnd',
        'TEST': {
            'MIRROR': 'default'
        },
        'PASSWORD': 'orjmiqsujp1l04c0',
        'HOST': 'en1ehf30yom7txe7.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',  # 'localhost'
        'PORT': '3306',

    }
}

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
LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "login"

STATIC_URL = '/static/'
MEDIA_URL = '/media/'


STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static', 'staticeducacion')]

STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media_cdn')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
"""
EMAIL_BACKEND = \ 
    'django.core.mail.backends.console.EmailBackend'
    """

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'andresarenas.kaiser@gmail.com'
EMAIL_HOST_PASSWORD = 'kaiser1234.'
