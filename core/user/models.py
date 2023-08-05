import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from config.settings import MEDIA_URL, STATIC_URL

class User(AbstractUser):
    if "WEBSITE_HOSTNAME" in os.environ:
        image=models.ImageField(upload_to=f'{MEDIA_URL}users/%Y/%m/%d', null=True, blank=True)
    else:
        image=models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)

    def get_image(self):
        if self.image:
            return self.image.url
        return '{}{}'.format(STATIC_URL, 'img/empty.webp')