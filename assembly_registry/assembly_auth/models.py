'''Creates UserProfile model'''
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from rest_framework.authtoken.models import Token


class Profile(models.Model):
    """Extention for user model.. as an extra field"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.CharField(max_length=128, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    User._meta.get_field('email')._unique = True  # @UndefinedVariable


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
