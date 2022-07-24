"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import environ
import os
# from oscar.defaults import *

env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

env.read_env('env/production.env')
if DEBUG:
    env.read_env('env/develop.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = []  # env('ALLOWED_HOSTS').split(',')


# Application definition

INSTALLED_APPS = [
    #'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ここから
    "scheduler.apps.SchedulerConfig",
    "common.apps.CommonConfig",
    "connectfam.apps.ConnectfamConfig",

    # # 以下の部分を追加
    # 'django.contrib.sites',
    # 'django.contrib.flatpages',
    # 'oscar.config.Shop',
    # 'oscar.apps.analytics.apps.AnalyticsConfig',
    # 'oscar.apps.checkout.apps.CheckoutConfig',
    # # 'oscar.apps.address.apps.AddressConfig',
    # 'oscar.apps.shipping.apps.ShippingConfig',
    # 'oscar.apps.catalogue.apps.CatalogueConfig',
    # 'oscar.apps.catalogue.reviews.apps.CatalogueReviewsConfig',
    # 'oscar.apps.communication.apps.CommunicationConfig',
    # 'oscar.apps.partner.apps.PartnerConfig',
    # 'oscar.apps.basket.apps.BasketConfig',
    # 'oscar.apps.payment.apps.PaymentConfig',
    # 'oscar.apps.offer.apps.OfferConfig',
    # 'oscar.apps.order.apps.OrderConfig',
    # # 'oscar.apps.customer.apps.CustomerConfig',
    # 'oscar.apps.search.apps.SearchConfig',
    # 'oscar.apps.voucher.apps.VoucherConfig',
    # 'oscar.apps.wishlists.apps.WishlistsConfig',
    # 'oscar.apps.dashboard.apps.DashboardConfig',
    # 'oscar.apps.dashboard.reports.apps.ReportsDashboardConfig',
    # 'oscar.apps.dashboard.users.apps.UsersDashboardConfig',
    # 'oscar.apps.dashboard.orders.apps.OrdersDashboardConfig',
    # 'oscar.apps.dashboard.catalogue.apps.CatalogueDashboardConfig',
    # 'oscar.apps.dashboard.offers.apps.OffersDashboardConfig',
    # 'oscar.apps.dashboard.partners.apps.PartnersDashboardConfig',
    # 'oscar.apps.dashboard.pages.apps.PagesDashboardConfig',
    # 'oscar.apps.dashboard.ranges.apps.RangesDashboardConfig',
    # 'oscar.apps.dashboard.reviews.apps.ReviewsDashboardConfig',
    # 'oscar.apps.dashboard.vouchers.apps.VouchersDashboardConfig',
    # 'oscar.apps.dashboard.communications.apps.CommunicationsDashboardConfig',
    # 'oscar.apps.dashboard.shipping.apps.ShippingDashboardConfig',

    # # 3rd-party apps that oscar depends on
    # 'widget_tweaks',
    # 'haystack',
    # 'treebeard',
    # 'sorl.thumbnail',
    # 'django_tables2',

    # # connectfam & oscarカスタマイズ
    # 'connectfam.address.apps.AddressConfig',
    # 'connectfam.customer.apps.CustomerConfig',

]

MIDDLEWARE = [
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # # 以下の部分を追加
    # 'oscar.apps.basket.middleware.BasketMiddleware',
    # 'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
                # # 次の4行を追加
                # 'oscar.apps.search.context_processors.search_form',
                # 'oscar.apps.checkout.context_processors.checkout',
                # 'oscar.apps.communication.notifications.context_processors.notifications',
                # 'oscar.core.context_processors.metadata',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'mysql',
        'PORT': '3306',
        # 'ATOMIC_REQUESTS': True,  # 追加
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'django',
#         'USER': 'root',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         # 'ATOMIC_REQUESTS': True,  # 追加
#     }
# }


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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# 追加
SITE_ID = 1

# 追加。日本円に対応。
# OSCAR_DEFAULT_CURRENCY = 'JPY'
# OSCAR_CURRENCY_FORMAT = '¤#,##0'

# connectfamの利用先を指定
# AUTH_USER_MODEL = "customer.User"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/html/static/'

""" Take this comment out to enable DebugToolbar
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'config.utils.show_toolbar',
}
"""

##########
# logging
##########

if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(asctime)s [%(levelname)s] %(process)d '
                          '%(pathname)s:%(lineno)d:%(funcName)s %(message)s',
            },
        },
        'handlers': {
            "file_handler": {
                "class": "logging.FileHandler",
                "level": "INFO",
                "formatter": "verbose",
                "filename": "test.log",
                "mode": "a",
                "encoding": "utf-8"
            }
        },
        'loggers': {
            'django': {
                'handlers': ['file_handler'],
                'level': 'INFO',
                'propagate': False,
            }
        }
    }

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# # 追加。メールアドレス認証に対応。
# AUTHENTICATION_BACKENDS = (
#     'oscar.apps.customer.auth_backends.EmailBackend',
#     'django.contrib.auth.backends.ModelBackend',
# )
