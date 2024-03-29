import os

# BASE_DIR = location with manage.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pxwl1csr@_2v3xsw@nin_3+ntf-f60$=6*0z0_7!6_2^ax9i0+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'finance.apps.FinanceConfig', #this app
    'django.contrib.admin',   # V default django apps V
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework'
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

ROOT_URLCONF = 'finance-site.urls'

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

WSGI_APPLICATION = 'finance-site.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3')        
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'mgrigola',
        'PASSWORD': 'boss',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'NAME': 'finance'
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    #  {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}
    # ,{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}
    # ,{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
    # ,{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}
]

# LOGIN_REDIRECT_URL = 'home'
# LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = ''
LOGOUT_REDIRECT_URL = 'index'

# AUTH_USER_MODEL = 'finance.User'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
