from lyft.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lyft_user',
        'USER': 'lyft_user',
        'HOST': 'db',
        'PORT': 5432,
    }
}
