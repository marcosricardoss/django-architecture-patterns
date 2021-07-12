from django.db import models

class Cronjob(models.Model):

    class Meta:        
        verbose_name = "Cronjob"        
        verbose_name_plural = 'Cronjobs'

    jobhash = models.SlugField(max_length=50, unique=True, blank=False)
    setting = models.TextField(blank=False)    
    created_at = models.DateTimeField("Created", auto_now_add=True)
    updated_at = models.DateTimeField("Updated", auto_now=True)                           

    def __str__(self) -> str:
        return self.setting