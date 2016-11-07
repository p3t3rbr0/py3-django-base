import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '3fcwiugtf+p#c+5_ep=e3x^7v&rrr6#h=_g=5z1a6=vg*(y$56'

DEBUG = True
ALLOWED_HOSTS = []

# Current project version, codename and sitename
VERSION = 'v0.4.2'
CODENAME = 'Clanga'
SITE_NAME = '127.0.0.1:8000' if DEBUG else 'http://djangobase.com'

# Apps
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

THIRD_PARTY_APPS = [
    'mptt',
    'ckeditor',
    'ckeditor_uploader'
]

if DEBUG:
    THIRD_PARTY_APPS += ['debug_toolbar']

LOCAL_APPS = [
    'apps.news',
    'apps.pages',
    'apps.feincms',
    'apps.gallery',
    'apps.accounts'
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

if DEBUG:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

ROOT_URLCONF = 'django_base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'django_base.wsgi.application'

# Database backend settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'djbase.db'),
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

# Language and locales settings
LANGUAGE_CODE = 'ru-RU'
LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)
TIME_ZONE = 'Europe/Moscow'  # 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Staticfiles setings
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Feincms static dir
FEINCMS_ADMIN_MEDIA = '/static/deps/feincms/'
FEINCMS_ADMIN_MEDIA_LOCATION = os.path.join(BASE_DIR, 'static/deps/feincms/')

# Session
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # One month

# Email SMTP backend settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_ALTERNATE = True
EMAIL_CODEPAGE = 'utf-8'
DEFAULT_FROM_EMAIL = 'DjangoBase project <no-reply@djbase.com>'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'djbaseproject@gmail.com'
EMAIL_HOST_PASSWORD = 'djbaseproject123'
EMAIL_PORT = 587

# Feedback
ADMINS = [('Peter P. Neuromantic', 'peter@neuro.com')]
SERVER_EMAIL = 'djbase@21stf'

# Custom user model settings
AUTH_USER_MODEL = 'accounts.CustomUser'

# CKEditor settings
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
CKEDITOR_UPLOAD_PATH = 'uploads/ckeditor/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = True
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'height': 400,
        'width': 960,
        'toolbar_Custom': [
            ['Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],
            ['Format', 'FontSize'],
            ['Bold', 'Italic', 'Underline'],
            [
                'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent',
                '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'
            ],
            ['Link', 'Unlink'],
            ['Image', 'Table'],
            ['Source', 'Maximize']
        ],
        'toolbarCanCollapse': True,
        'extraPlugins': 'tableresize'
    },
}

# Thumbnails defaults settings
THUMBS_QUALITY = 80
THUMBS_FORMAT = 'JPEG'
