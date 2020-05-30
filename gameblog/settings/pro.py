from .base import *



DEBUG = False

DATABASES = {
    'default': {
	   	'ENGINE': 'django.db.backends.postgresql_psycopg2',
	    'NAME':'ddloo1h4pm5k6c',
	    'USER':'cdhsujndbomlra',
	    'PASSWORD':'384c1f1b964897a8420a931f434d0fa0fc48357132c23b128d7c47dac20e73c6',
	    'HOST':'ec2-54-88-130-244.compute-1.amazonaws.com',
	    'PORT':'5432',
    }
}


db_from_env=dj_database_url.config()
DATABASES['default'].update(db_from_env)


#Настройки для связи Heroku с облачным сервисом Дропбокс, который хранит картинки.
DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'

DROPBOX_OAUTH2_TOKEN = 'VeNVl9rVshAAAAAAAAAAFbUqDiFEf3czo0gKHE4nE9YyEmA428nn6Y99A45_IHQS'

DROPBOX_ROOT_PATH = 'media/'


ADMINS = (('Renar', 'imperecdiego@gmail.com'),)