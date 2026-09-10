"""
Django settings for Orthobest Care Hub project.
Modern, Gen-Z styled Kenyan e-commerce platform for Orthopedic & Rehabilitation Products.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-secret-key-orthobestcarehub-2026-kenya')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,orthobestcarehub.co.ke,www.orthobestcarehub.co.ke,orthobestcarerehab.co.ke').split(',') if h.strip()]

CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost:8000,http://127.0.0.1:8000,https://orthobestcarehub.co.ke,https://www.orthobestcarehub.co.ke').split(',') if o.strip()]

# Application definition
INSTALLED_APPS = [
    # Django Unfold Admin (Must be placed before django.contrib.admin)
    'unfold',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',

    # Rich Text Editor
    'django_ckeditor_5',

    # Custom Modular Apps
    'apps.core.apps.CoreConfig',
    'apps.products.apps.ProductsConfig',
    'apps.cart.apps.CartConfig',
    'apps.orders.apps.OrdersConfig',
    'apps.payments.apps.PaymentsConfig',
    'apps.accounts.apps.AccountsConfig',
    'apps.content_hub.apps.ContentHubConfig',
    'apps.leads.apps.LeadsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'apps.core.middleware.LegacyDomainRedirectMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'orthobestcarehub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site_settings_context',
                'apps.cart.context_processors.cart_context',
                'apps.products.context_processors.wishlist_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'orthobestcarehub.wsgi.application'

# ==============================================================================
# DATABASE CONFIGURATION (MariaDB / MySQL on Shared Hosting + Dev SQLite Fallback)
# ==============================================================================
DATABASE_URL = os.environ.get('DATABASE_URL')
DB_NAME = os.environ.get('DB_NAME')
DB_ENGINE = os.environ.get('DB_ENGINE', 'django.db.backends.mysql')

if DATABASE_URL:
    import urllib.parse
    url = urllib.parse.urlparse(DATABASE_URL)
    engine_map = {
        'mysql': 'django.db.backends.mysql',
        'mariadb': 'django.db.backends.mysql',
        'postgres': 'django.db.backends.postgresql',
        'postgresql': 'django.db.backends.postgresql',
        'sqlite': 'django.db.backends.sqlite3',
    }
    DATABASES = {
        'default': {
            'ENGINE': engine_map.get(url.scheme, 'django.db.backends.mysql'),
            'NAME': url.path[1:],
            'USER': url.username or '',
            'PASSWORD': url.password or '',
            'HOST': url.hostname or 'localhost',
            'PORT': url.port or (3306 if url.scheme in ('mysql', 'mariadb') else 5432),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            } if url.scheme in ('mysql', 'mariadb') else {},
        }
    }
elif DB_NAME or not DEBUG:
    # Production Shared Hosting MariaDB default
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': os.environ.get('DB_NAME', 'orthobestcare'),
            'USER': os.environ.get('DB_USER', 'orthobestuser'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    # Local Development SQLite Fallback
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==============================================================================
# CACHING SYSTEM (Database Cache for shared hosting `createcachetable`)
# ==============================================================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': os.environ.get('CACHE_TABLE', 'orthobest_cache_table'),
        'TIMEOUT': int(os.environ.get('CACHE_TIMEOUT', 300)),
        'OPTIONS': {
            'MAX_ENTRIES': int(os.environ.get('CACHE_MAX_ENTRIES', 5000)),
        }
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images) & WhiteNoise
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (Product uploads, banners, avatars)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication URLs
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:dashboard'
LOGOUT_REDIRECT_URL = 'core:home'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email backend configuration (Django SMTP backend for shared hosting)
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'mail.orthobestcarehub.co.ke')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 465))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'False').lower() in ('true', '1', 't')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'True').lower() in ('true', '1', 't')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'Orthobest Care Hub <info@orthobestcarehub.co.ke>')

# Security & Session Settings
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 days
SESSION_SAVE_EVERY_REQUEST = False
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Production SSL & Reverse Proxy Security
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() in ('true', '1', 't')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Custom 404/500/403 handlers
handler404 = 'apps.core.views.custom_404_view'
handler500 = 'apps.core.views.custom_500_view'
handler403 = 'apps.core.views.custom_403_view'

# ==============================================================================
# DJANGO CKEDITOR 5 CONFIGURATION
# ==============================================================================
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote'],
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': [
            'heading', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
            '|', 'bulletedList', 'numberedList', 'todoList',
            '|', 'outdent', 'indent',
            '|', 'insertTable',
            '|', 'undo', 'redo'
        ],
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells'],
        },
    }
}

# ==============================================================================
# DJANGO UNFOLD CONFIGURATION — CUSTOM BRANDED NAVY (#01174E) & GOLD (#FBD420)
# ==============================================================================
UNFOLD = {
    "SITE_TITLE": "Orthobest Care Hub Admin",
    "SITE_HEADER": "Orthobest Care Hub",
    "SITE_SUBHEADER": "Orthopedic & Rehabilitation Administration",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: "/static/images/placeholder.svg",
        "dark": lambda request: "/static/images/placeholder.svg",
    },
    "SITE_LOGO": {
        "light": lambda request: "/static/images/placeholder.svg",
        "dark": lambda request: "/static/images/placeholder.svg",
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: "/static/images/placeholder.svg",
        },
    ],
    "COLORS": {
        "primary": {
            "50": "241 245 254",
            "100": "220 231 253",
            "200": "185 208 250",
            "300": "135 174 246",
            "400": "79 133 239",
            "500": "36 94 227",
            "600": "18 67 197",
            "700": "10 47 155",
            "800": "5 31 110",
            "900": "1 23 78",    # Official Deep Navy #01174E
            "950": "0 12 46",
        },
    },
    "STYLES": [
        lambda request: "/static/css/admin_custom.css",
    ],
}
