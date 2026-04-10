from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ Django
SECRET_KEY = os.environ.get("DJANGO_SKEY", '')

# Дебаг (показ ошибок)
DEBUG = os.environ.get('DEBUG', False)

# Поддерживаемые хосты
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')


# Application definition
# Встроенные в Django приложения
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Список сторонних приложений
THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
]

# Список локальных приложений
LOCAL_APPS = [
    # APIs
    'apps.APIs.notes',
    'apps.APIs.cars',
]

# Общий список
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# Список для обработки запросов 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# Корневой URL-файл проекта
ROOT_URLCONF = 'config.urls'

# Конфигурация шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# Конфигурация БД
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', ''),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', 5432),
        'ATOMIC_REQUESTS': True,
    }
}


# Валилаторы паролей
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


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/' # статические файлы
STATIC_ROOT = BASE_DIR / 'staticfiles' # сборка всех статических файлов



# Настройки DRF (Django Rest Framework)
REST_FRAMEWORK = {
    'DEFAULT_PREMISSION_CLASSES': [
        'rest_framework.premissions.AllowAny', # Разрешить доступ всем
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle', # Ограничение запросов для анонов
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour', # Лимит запросов для анонимных пользователей 
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer', # рендеринг в JSON
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser', # парсинг JSON данных
    ], 
}


# Настройка CORS для разработки и продакшена
if DEBUG: # Если разработка, то пропускаем все домены
    CORS_ALLOW_ALL_ORIGINS = True 
else: # Если продакшен - только разрешенные источники
    CORS_ALLOWED_ORIGINS = [ 
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ]


# Настройка безопасности
SECURE_BROWSER_XSS_FILTER = True # Защита от XSS-атак (нем не смогут js-скрипт в форму, инпут вписать в шаблонах)
SECURE_CONTENT_TYPE_NOSNIFF = True # Запрет MIME-типов (exeшники чтобы не принимали на файлах)
X_FRAME_OPTIONS = 'DENY'


# Настройки логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO', # Уровень логирования
            'class': 'logging.FileHandler', # Логирование в файл
            'filename': BASE_DIR / 'debug.log', # Путь к файлу логирования
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}