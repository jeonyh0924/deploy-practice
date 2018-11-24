from .base import *

DEBUG = True

WSGI_APPLICATION = 'config.wsgi.application'

secrets = json.load(open(os.path.join(SECRETS_DIR, 'dev.json')))

DATABASES = secrets['DATABASES']