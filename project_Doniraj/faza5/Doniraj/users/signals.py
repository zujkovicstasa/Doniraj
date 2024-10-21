#Autor: Matija Milic 2021/0088
import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import User

@receiver(pre_save, sender=User)
def delete_old_image(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = User.objects.get(pk=instance.pk).image
    except User.DoesNotExist:
        return False

    new_image = instance.image
    if old_image and old_image.url != new_image.url and old_image.name != 'profile_pics/profil.png':
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)