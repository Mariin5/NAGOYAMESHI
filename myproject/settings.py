"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f4v1xe4*gzy$fg$z#oa0=a7372__u6#v-f%o4axwfyou6pj9o%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['nagoyameshi-marina-32890ff7fdd2.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    "nagoyameshi.apps.NagoyameshiConfig",
    "accounts.apps.AccountsConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stripe',
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
ACCOUNT_AUTHENTICATION_METHOD   = "email"
ACCOUNT_USERNAME_REQUIRED       = False
ACCOUNT_EMAIL_VARIFICATION  = "mandatory"
ACCOUNT_EMAIL_REQUIRED      = True

#DEBUGがTrueのとき、メールの内容は全て端末に表示させる
if DEBUG:
    EMAIL_BACKEND   = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND   = "django.core.mail.backends.console.EmailBackend"


LOGIN_REDIRECT_URL  = "/"
LOGOUT_REDIRECT_URL = "login" # urls.pyのnameを参照している。

AUTH_USER_MODEL = 'accounts.CustomUser'
ACCOUNT_FORMS   = { "signup":"accounts.forms.SignupForm"}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
#STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# 静的ファイルの読み込み設定がwhitenoiseに影響が及ぶので、デバッグ時にのみ有効にしておく。
if DEBUG:
    STATICFILES_DIRS = [ BASE_DIR / "static" ]

#Stripe API Key
if "STRIPE_PUBLISHABLE_KEY" in os.environ and "STRIPE_API_KEY" in os.environ and "STRIPE_PRICE_ID" in os.environ:
    STRIPE_PUBLISHABLE_KEY  = os.environ["STRIPE_PUBLISHABLE_KEY"]
    STRIPE_API_KEY          = os.environ["STRIPE_API_KEY"]
    STRIPE_PRICE_ID         = os.environ["STRIPE_PRICE_ID"]
'''
else:
    from . import secret_settings

    STRIPE_API_KEY          = secret_settings.STRIPE_API_KEY
    STRIPE_PUBLISHABLE_KEY  = secret_settings.STRIPE_PUBLISHABLE_KEY
    STRIPE_PRICE_ID         = secret_settings.STRIPE_PRICE_ID
'''






if not DEBUG:

    #INSTALLED_APPSにcloudinaryの追加
    INSTALLED_APPS.append('cloudinary')
    INSTALLED_APPS.append('cloudinary_storage')

    ALLOWED_HOSTS = ['nagoyameshi-marina-32890ff7fdd2.herokuapp.com']
    CSRF_TRUSTED_ORIGINS    = [ "https://nagoyameshi-marina-93dfff473afb.herokuapp.com" ]

    
    
    # 静的ファイル配信ミドルウェア、whitenoiseを使用。※ 順番不一致だと動かないため下記をそのままコピーする。
    MIDDLEWARE = [ 
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]

    # 静的ファイル(static)の存在場所を指定する。
    STATIC_ROOT = BASE_DIR / 'static'


    # DBの設定
    '''
    DATABASES = { 
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': os.environ["DATABASE_NAME"],
                'USER': os.environ["DATABASE_USER"],
                'PASSWORD': os.environ["DATABASE_PASSWORD"],
                'HOST': os.environ["DATABASE_HOST"],
                'PORT': '5432',
                }
            }
    '''
    DATABASES = { 
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': os.environ["DATABASE_NAME"],
                'USER': os.environ["DATABASE_USER"],
                'PASSWORD': os.environ["DATABASE_PASSWORD"],
                'HOST': os.environ["DATABASE_HOST"],
                'PORT': '5432',
                }
            }

    #DBのアクセス設定
    import dj_database_url

    db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
    DATABASES['default'].update(db_from_env)
    

    #cloudinaryの設定
    CLOUDINARY_STORAGE = { 
            'CLOUD_NAME': os.environ["CLOUDINARY_CLOUD_NAME"], 
            'API_KEY'   : os.environ["CLOUDINARY_API_KEY"], 
            'API_SECRET': os.environ["CLOUDINARY_API_SECRET"],
            "SECURE"    : True,
            }

    #これは画像だけ(上限20MB)
    #DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

    #これは動画だけ(上限100MB)
    #DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.VideoMediaCloudinaryStorage'

    #これで全てのファイルがアップロード可能(上限20MB。ビュー側でアップロードファイル制限するなら基本これでいい)
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'


