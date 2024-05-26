from django.db import models
from django.urls import reverse


class SpaceNews(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to="space_news/%Y/%m/%d/")
    time_create = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"news_slug": self.slug})

    class Meta:
        verbose_name = "news"
        verbose_name_plural = "space news"
        ordering = ["-time_create"]
