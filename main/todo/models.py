"""Models of the 'todo' app."""

from django.db import models
from django.utils import timezone
from django.urls import reverse


class Task(models.Model):
    """ Task's model class."""

    title = models.CharField(max_length=250)    
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deadline_at = models.DateTimeField(default=timezone.now) # models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self, *args, **kwargs):
        return reverse("todo:detail", kwargs={"id":self.id})    