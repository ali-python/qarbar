from django.db import models
from core.models import DatedModel

class News(DatedModel):
    title = models.CharField(max_length=200)
    news_image = models.ImageField(upload_to='news_images/')
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
