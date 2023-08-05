import os

from .settings import * #importamos todo
from .settings import BASE_DIR # importamos la ruta de inicio

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

DEBUG = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Add whitenoise middleware after the security middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

conn_str = os.environ['AZURE_MYSQL_CONNECTIONSTRING']

conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}

#AZURE_MYSQL_CONNECTIONSTRING=dbname=nombreBD host=elHost port=3306 sslmode=require user=usuario password=pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': conn_str_params['dbname'],
        'HOST': conn_str_params['host'],
        'USER': conn_str_params['user'],
        'PASSWORD': conn_str_params['password'],
    }
}

# alamacenamiento con Azure

azure_storage_blob = os.environ['AZURE_STORAGE_BLOB']
azure_storage_blob_parametros = {parte.split(' = ')[0]:parte.split(' = ')[1] for parte in azure_storage_blob.split('  ')}

AZURE_CONTAINER = azure_storage_blob_parametros['container_name']
AZURE_ACCOUNT_NAME = azure_storage_blob_parametros['account_name']
AZURE_ACCOUNT_KEY = azure_storage_blob_parametros['account_key']
STORAGES = {
    "default": {"BACKEND": "storages.backends.azure_storage.AzureStorage"},
    "staticfiles": {"BACKEND": "custom_storage.custom_azure.PublicAzureStaticStorage"},
    "media": {"BACKEND": "custom_storage.custom_azure.PublicAzureMediaStorage"},
}
#AZURE_STORAGE_BLOB = account_name = contenedordasix  container_name = django-dasix  account_key = vT1l/DKQHh/tap5/GK0LjmtA1W4SqTDA1IbL7M+iYit1FALrry0kmTz3BEDqsqB+PnMimTxouZQi+AStUN9fMw==