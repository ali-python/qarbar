# models.py
from django.db import models
from core.models import DatedModel
from ckeditor.fields import RichTextField

class News(DatedModel):
    title = models.CharField(max_length=200)
    news_image = models.CharField(max_length=250, null=True, blank=True)
    description = RichTextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
