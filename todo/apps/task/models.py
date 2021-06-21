"""Models of the 'task' app."""

from django.db import models
from django.urls import reverse

from utils.models import CreationModificationDateMixin

class Task(CreationModificationDateMixin):
    """ Task's model class."""

    class Meta:
        ordering = ['deadline_at']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    title = models.CharField(max_length=250)    
    description = models.TextField(null=True, blank=True)    
    deadline_at = models.DateTimeField("Deadline", help_text="The deadline date of the task")
    finished_at = models.DateTimeField("Finished", null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self, *args, **kwargs):
        return reverse("task:detail", kwargs={"id":self.id})    