from django.db import models
from django.urls import reverse

from utils.models import CreationModificationDateMixin


class Tag(CreationModificationDateMixin):
    """Tag's model class."""

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    slug = models.SlugField(max_length=50, unique=True, blank=False)

    def __str__(self) -> str:
        return self.slug

    def get_absolute_url(self, *args, **kwargs):
        return reverse("task:detail", kwargs={"id": self.id})
