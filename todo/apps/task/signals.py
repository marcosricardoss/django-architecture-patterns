import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from .models import Task


logger = logging.getLogger('django')
         

@receiver(post_save, sender=Task)
def news_save_handler(sender, **kwargs):    
    if settings.DEBUG:
        logger.info(f"{kwargs['instance']} saved.")                        


@receiver(post_delete, sender=Task)
def news_delete_handler(sender, **kwargs):        
    if settings.DEBUG:
        logger.info(f"{kwargs['instance']} deleted.")             
