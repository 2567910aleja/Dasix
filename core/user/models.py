import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict
from config.settings import MEDIA_URL, STATIC_URL

AZURE_STATIC="https://contenedordasix.blob.core.windows.net/django-dasix"+STATIC_URL

class User(AbstractUser):
    if "WEBSITE_HOSTNAME" in os.environ:
        image=models.ImageField(upload_to=f'{MEDIA_URL}users/%Y/%m/%d', null=True, blank=True)
    else:
        image=models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)

    def get_image(self):
        if self.image:
            return self.image.url
        if "WEBSITE_HOSTNAME" in os.environ:
            return '{}{}'.format(AZURE_STATIC, 'img/empty.png')
        else:
            return '{}{}'.format(STATIC_URL, 'img/empty.png')
    
    def toJSON(self):
        item={'username':self.username,"image":self.get_image()}
        return item