from django.db import models

class CreationModificationDateMixin(models.Model):
    """
    Abstract base class with a creation
    and modification date and time
    """
    class Meta:
        abstract = True    
    
    created_at = models.DateTimeField("Created", auto_now_add=True)
    updated_at = models.DateTimeField("Updated", auto_now=True)
    