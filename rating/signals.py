from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Restaurant
from user.models import Reviews

# @receiver(post_save,sender=User)
# def create_profile(sender,instance,created,**kwargs):
#     if created:
#         Restaurant.objects.create(user=instance)


# @receiver(post_save,sender=User)
# def save_profile(sender,instance,**kwargs):
#     instance.information.save()


# @receiver([post_save, post_delete, post_update], sender=Reviews)
# def update_score(sender, **kwargs):
#     instance = kwargs.get('instance')
#     if instance:


# @receiver(post_save,sender=User)
# def save_profile(sender,instance,**kwargs):
#     instance.information.save()
    
# @receiver([post_save, post_update], sender=Restaurant)
# def update_score(sender, **kwargs):
#     instance = kwargs.get('instance')
#     if instance:
