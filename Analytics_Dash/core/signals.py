from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from core.models import UserRole

@receiver(post_save, sender=User)
def create_user_role(sender, instance, created, **kwargs):
    U = UserRole.objects.get_or_create(user=instance)
    print('UserRole created')
    
