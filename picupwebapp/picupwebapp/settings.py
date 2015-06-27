# Django settings for classifiedcoin project.
import os
PROJECT_DIR = os.path.dirname(__file__)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# BELOW IS A DEFAULT KEY - DIFFERENT THAN https://picup.it/ one.
SECRET_KEY = '2CH$NAGEM#3ORdI3%2CH$NAGEM#3ORdI3%2CH$NAGEM#3ORdI3%2CH$NAGEM#3ORdI3%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, "templates"),
)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'social.apps.django_app.default',
    'foundation',
    'picupwebapp.picture',
    'picupwebapp.picprofile',

)

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'picupwebapp.urls'

WSGI_APPLICATION = 'picupwebapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/picup.db',
    }
}
AUTHENTICATION_BACKENDS = (
      'social.backends.open_id.OpenIdAuth',
      'social.backends.persona.PersonaAuth',
      'social.backends.github.GithubOAuth2',
      'django.contrib.auth.backends.ModelBackend',
  )
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
        os.path.join(PROJECT_DIR, "static/"),
)


MEDIA_ROOT = os.path.join(PROJECT_DIR, "../pictures")
MEDIA_URL = '/media/'

# PICUP custom settings
PICUP_THUMB_SIZE = (210,210)
PICUP_MEDIUM_SIZE = (640,640)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'picup',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'picup',
        'PASSWORD': 'picup_development',
        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}
ADMINS = (('bluszcz@bluszcz.net',))

TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth',
 'django.core.context_processors.debug',
 'django.core.context_processors.i18n',                                                                                                                                                       
 'django.core.context_processors.media',                                                                                                                                                      
 'django.core.context_processors.static',                                                                                                                                                     
 'django.core.context_processors.tz',                                                                                                                                                         
 'django.contrib.messages.context_processors.messages',
 'picupwebapp.picprofile.context_processors.picup_profile',
 ) 
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/picup-debug.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

from logging.handlers import SysLogHandler 
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
        
        'syslog':{
            'address': '/dev/log',
            'class': 'logging.handlers.SysLogHandler',
            'facility': SysLogHandler.LOG_LOCAL1, 
        }
    },


    
    'loggers': {

        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
'': {
            'handlers': ['syslog'],
            'level': 'DEBUG',
        }


    },
   'syslog':{
        'level':'INFO',
        'class': 'logging.handlers.SysLogHandler',
        'formatter': 'verbose',
        'facility': 'local1',
        'address': '/dev/log',
    },


}
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
SOCIAL_AUTH_GITHUB_KEY = GITHUB_APP_ID = ''
SOCIAL_AUTH_GITHUB_SECRET = GITHUB_API_SECRET = ''
GITHUB_EXTENDED_PERMISSIONS = ['email']

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is were emails and domains whitelists are applied (if
    # defined).
    'social.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    'social.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address.
    'social.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social.pipeline.user.create_user',

    # Create the record that associated the social account with this user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social.pipeline.user.user_details'
)

# Used for some homepage calculations
RECOMMENDED_ROWS = 4 

PICUP_NAME = 'PicUp.It'
PICUP_URL = PICUP_NAME.lower()

from settings_locals import *