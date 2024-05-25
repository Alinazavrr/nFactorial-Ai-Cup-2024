from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from django.contrib.auth.models import User


# @receiver(post_save, sender=User)
# def create_custom_user(sender, instance, created, **kwargs):
#     if created:
#         CustomUser.objects.create(user=instance)



