from django.conf import settings
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


class Comment(models.Model):
    DoesNotExist = None
    objects = None
    news = models.ForeignKey(
        SpaceNews, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.author} on "{self.news}"'

    class Meta:
        ordering = ["-time_create"]


class Constellation(models.Model):
    objects = None

    def upload_img(self, filename):
        return f"constellations/{self.slug}/{filename}"

    name = models.CharField(max_length=100, db_index=True, unique=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)
    image = models.ImageField(blank=True, upload_to=upload_img)
    area = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True)
    quadrant = models.CharField(max_length=50, blank=True, db_index=True)
    description = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
