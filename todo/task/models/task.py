import uuid

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from utils.models import CreationModificationDateMixin

from .tag import Tag


class Task(CreationModificationDateMixin):
    """Task's model class."""

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
    
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    deadline_at = models.DateTimeField(
        "Deadline", help_text="The deadline date of the task"
    )
    finished_at = models.DateTimeField("Finished", null=True, blank=True)
    tags = models.ManyToManyField(
        Tag,
        help_text=mark_safe(
            "<small>Can be added by the Django administration panel</small>"
        ),
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.title

    @property
    def is_past_due(self, *args, **kwargs):
        if (self.finished_at and self.finished_at > self.deadline_at) or (
            timezone.now() > self.deadline_at
        ):
            return True
        return False

    @property
    def tag_list(self, *args, **kwargs):
        return self.tags.all()

    def get_absolute_url(self, *args, **kwargs):
        return reverse("task:detail", kwargs={"id": self.id})
