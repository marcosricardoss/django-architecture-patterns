from django.db import models

class Cronjob(models.Model):

    jobhash = models.SlugField(max_length=50, unique=True, blank=False)
    setting = models.TextField(blank=False)    

    class Meta:        
        verbose_name = "Cronjob"        
        verbose_name_plural = 'Cronjobs'                       

    def __str__(self) -> str:
        return self.setting