import os

USE_MYSQL = True
USE_CACHES = True
USE_LOGGING = False


# ################### get_set_setting ####################
# get and set attribute from the file settings
def get_setting(name, default=None):
    from django.conf import settings
    return getattr(settings, name, default)


def set_setting(name, default=None):
    from django.conf import settings
    return setattr(settings, name, default)


# ################### BASE_DIR #######################
BASE_DIR = get_setting('BASE_DIR')


# ################### MIDDLEWARE #######################
middleware_lst = ['task_app.middleware.auth.AuthMiddleware', ]

MIDDLEWARE = get_setting('MIDDLEWARE')
# MIDDLEWARE.extend(middleware_lst)


# ################ INSTALLED_APPS #####################
app_lst = ['rbac', 'crud', 'web']

INSTALLED_APPS = get_setting('INSTALLED_APPS')
INSTALLED_APPS.extend(app_lst)


# #################AUTH_USER_MODEL######################
AUTH_USER_MODEL = 'web.User'
USER_RBAC = 'rbac.models.User'


# ##################### DATABASE Mysql ################
if USE_MYSQL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'BaseApp',
            'USER': 'root',
            'PASSWORD': 'root!23456',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }

# ############# Redis settings default 0-15 ###########
if USE_CACHES:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379/0',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'PASSWORD': 'root123',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 100,
                },

            },
        },
        'verify_code': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379/1',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'PASSWORD': 'root123',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 100,
                },

            },
        },
        'celery': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379/1',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'PASSWORD': 'root123',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 100,
                },

            },
        }
    }


# ######################## CELERY ############################
CELERY_TASKS = 'celery_tasks'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/2'


# ######################## EMAIL ############################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25

EMAIL_HOST_USER = '541726975@qq.com'
EMAIL_HOST_PASSWORD = 'cys20041487'
EMAIL_FROM = 'BugTracer<541726975@qq.com>'

# #################### Logging #######################
if USE_LOGGING:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format':
                    '%(levelname)s %(asctime)s %(pathname)s %(module)s %(lineno)s %(process)d %(thread)d %(message)s'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['default'],
                'propagate': True,
                'level': 'DEBUG',
                'filters': ['special']
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'filename': ['require_debug_true'],
                'class': 'logging.StreamHandler',
                'maxBytes': 1024 * 1024 * 300,
                'formatter': 'simple',

            },
            'default': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(BASE_DIR, 'logs/bugTracer.log'),
                'maxBytes': 1024 * 1024 * 300,
                'backupCount': 10,
                'formatter': 'verbose',
                'filters': ['special']
            }
        },
        'filters': {
            'special': {
                '()': 'web.my_logging.ContextFilter'
            }
        },
    }


# #################LOGIN_URL############################
# Specify the redirect address where the user is not logged in
# LOGIN_URL = 'web/signin_password'


# ################ WHITE_REGEX_URL ######################
WHITE_REGEX_URL_LIST = [
    "/register/",
    "/send/sms/",
    "/signin/",
    "/images/code/",
    "/index/",
    "/price/",
]


# ######################### STATICFILES_DIRS #####################
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


# ######################### TEMPLATES ############################
# DIRS
# templates_dir = [f'{ BASE_DIR }/static', f'{ BASE_DIR }/templates', ]
templates_dir = [BASE_DIR / 'static',
                 BASE_DIR / 'templates', ]

templates = get_setting('TEMPLATES')
templates[0]['DIRS'].extend(templates_dir)

# OPTIONS / context_processors
new_context_processors = ''
templates[0]['OPTIONS']['context_processors'].extend(new_context_processors)


# ######################### TEMPLATES ############################
# LOGIN_REDIRECT_URL =


# ######################### MEDIA ################################
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)


# ###################### ALLOWED_HOSTS ############################
if get_setting('DEBUG'):
    HOSTS = ['bookstore.com', '127.0.0.1']
    ALLOWED_HOSTS = get_setting('ALLOWED_HOSTS')
    ALLOWED_HOSTS.extend(HOSTS)




