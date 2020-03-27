"""
Django settings for P2PLoan project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
from django import template
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR) #简化导入目录包的路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y5&02(b^g1^5r*$#93x%z(wi@cdn&h_n738zt1*kib-cvbte_*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'users.UserProfile'
# Application definition

AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
    # 'users.views.'
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}


INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'crispy_forms',
    'xadmin',
    'captcha',
    'certification',
    'rest_framework',
    'users.templatetags',
    'business',
    'el_pagination',
    'webnews',
    'DjangoUeditor',

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

ROOT_URLCONF = 'P2PLoan.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'P2PLoan.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "p2ploan",
        'USER': 'root',
        'PASSWORD': "MYSQL366459",
        'HOST': "127.0.0.1",
        "OPTIONS": {"init_command": "SET default_storage_engine=INNODB;"}
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/


LANGUAGE_CODE = 'zh-hans'

#时期
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

#使用本地时间
USE_TZ = False





# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

#静态文件目录
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static/"),
)



# 邮箱配置

#发送邮箱配置
EMAIL_HOST = "smtp.163.com"
EMAIL_PORT= 25
#发送方账号
EMAIL_HOST_USER = "pub_fei_xiang2017@163.com"
#第三方授权登录密码
EMAIL_HOST_PASSWORD = "SHOUQUAN366459"
EMAIL_USE_TLS = False
EMAIL_FROM = "pub_fei_xiang2017@163.com"



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# 验证码
CAPTCHA_IMAGE_SIZE = (80, 30)   # 设置 captcha 图片大小
CAPTCHA_LENGTH = 4   # 字符个数
CAPTCHA_TIMEOUT = 5   # 超时(minutes)
# CAPTCHA_FONT_SIZECAPT = '20'
CAPTCHA_FONT_SIZECAPT = '10'


#手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"


# CAPTCHA_OUTPUT_FORMAT = '%(image)s %(text_field)s %(hidden_field)s '
# CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null', # 没有样式
#     # 'captcha.helpers.noise_arcs', # 线
#     # 'captcha.helpers.noise_dots', # 点
# )
# # 图片中的文字为随机英文字母，如 mdsh
# # CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
#  # 图片中的文字为数字表达式，如2+2=
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
# # 超时(minutes)
# CAPTCHA_TIMEOUT = 1