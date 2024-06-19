
from pathlib import Path
from django.contrib.messages import constants as messages
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-bt0n4op$p^_q*27f2hqhc51!+=f6e=h3by=dq(#v=)mzke=y+#"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []




MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Application definition

INSTALLED_APPS = [
 
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.humanize',
    'ckeditor',
    "account",
    "home",
    "group",
    "post",
    "user",
    "chat",
    "search",
]

ASGI_APPLICATION = "discussit.routing.application"

CHANNEL_LAYERS = {
    'default':{
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'group.views.BlockedMemberMiddleware',
    'group.views.PrivateGroupMiddleware'
]

ROOT_URLCONF = "discussit.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / 'templates'
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'django.template.context_processors.request',
                'chat.context_processors.unread_message_count',
                'user.context_processors.group_request',
                'group.context_processors.recent_groups'
                
            ],
        },
    },
]




# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "discussit",
        "USER": "postgres",
        "PASSWORD":"admin",
        "HOST":"localhost",
        "PORT":""
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL="account.User"

LOGIN_URL = 'account:login'
CKEDITOR_CONFIGS = {
    'default': {
        'width': '128%',
        'toolbar': 'Custom',
    
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline','Strikethrough', '-', 'Link', 'CodeSnippet', '-', 
             'NumberedList', 'BulletedList', 'HorizontalRule', '-',


             ],
        ], 'extraPlugins': 'codesnippet'
    }
}