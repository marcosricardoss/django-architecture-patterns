"""Models of the 'task' app."""

from django.db import models
from django.utils import timezone
from django.urls import reverse


class Task(models.Model):
    """ Task's model class."""

    title = models.CharField(max_length=250)    
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField("Created", default=timezone.now)
    updated_at = models.DateTimeField("Updated", null=True, blank=True)
    deadline_at = models.DateTimeField("Deadline", help_text="The deadline date of the task") # models.DateTimeField()
    finished_at = models.DateTimeField("Finished", null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self, *args, **kwargs):
        return reverse("task:detail", kwargs={"id":self.id})    