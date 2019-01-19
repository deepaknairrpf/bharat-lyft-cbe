from lyft.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lyft',
        'USER': 'lyft_user',
        'PASSWORD': 'lyft_user',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
