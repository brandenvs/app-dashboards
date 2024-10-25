from pathlib import Path
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
ENV_PATH = os.path.join(BASE_DIR, '.env')
config._find_file(ENV_PATH)

# Quick-start development settings
SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

# Application definition

INSTALLED_APPS = [
    'users',
    'standalone',
    'hyperion',
    'portal',
    'user_auth',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',    
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Loading test/prod settings based on ENV settings
# ENV = os.environ.get('ENV')

# Cookies
SESSION_COOKIE_SECURE = True

'''APPLICATION SECURITY SETTINGS'''
# CORS Policy
CORS_ALLOW_ALL_ORIGINS = True

# CSRF Tokenization
CSRF_TRUSTED_ORIGINS = ['https://br-code.bcodelabs.com']
CSRF_COOKIE_SECURE = True

ROOT_URLCONF = 'labSite.urls'

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

WSGI_APPLICATION = 'labSite.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_URL = '/static/'

STATIC_ROOT = config('STATIC_ROOT')

STATICFILES_DIRS = [
    os.path.join(STATIC_ROOT, 'logos'),
    os.path.join(STATIC_ROOT, 'favicon'),
    os.path.join(STATIC_ROOT, 'js'),
    os.path.join(STATIC_ROOT, 'css'),
    os.path.join(STATIC_ROOT, 'images'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Google auth

# Define the scope for the credentials
SCOPE = ['https://www.googleapis.com/auth/cloud-platform']

# Path to the credentials file
CREDS_FILE = os.path.join(BASE_DIR, 'credentials', 'hd-testing.json')
