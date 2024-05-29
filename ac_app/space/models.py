from django.conf import settings
from django.core.validators import FileExtensionValidator
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

    def get_absolute_url(self):
        return reverse("constellation_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["name"]


class SpectralClass(models.Model):
    name = models.CharField(max_length=50, db_index=True, unique=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)
    image = models.FileField(
        blank=True,
        upload_to="Spectrum_svg/",
        validators=[FileExtensionValidator(["png", "svg"])],
    )
    color = models.CharField(max_length=50)
    temperature = models.CharField(max_length=50)
    features = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Spectral classes"
        ordering = ["id", "name"]


class Star(models.Model):
    def upload_img(self, filename):
        return f"stars/{self.slug}/{filename}"

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to=upload_img)
    time_create = models.DateTimeField(auto_now_add=True)
    spectrum = models.ForeignKey(SpectralClass, on_delete=models.PROTECT)
    constellation = models.ForeignKey(
        Constellation, on_delete=models.PROTECT, blank=True, null=True, default=None
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('star_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ["name", "spectrum"]


class StarCharacteristics(models.Model):
    AGE_UNITS_CHOICES = (
        (1, "Million Years"),
        (2, "Billion Years")
    )

    star = models.OneToOneField(Star, on_delete=models.CASCADE, blank=True, null=True)
    full_spectrum = models.CharField(max_length=50, blank=True)
    galaxy = models.CharField(max_length=100, blank=True)
    apparent_magnitude = models.CharField(max_length=50, blank=True)
    absolute_magnitude = models.CharField(max_length=50, blank=True)
    distance = models.CharField(max_length=100, blank=True)
    radial_velocity = models.CharField(max_length=50, blank=True)
    mass = models.FloatField(verbose_name="Mass (in solar masses)", null=True, blank=True)
    age = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    age_unit = models.IntegerField(
        blank=True,
        choices=AGE_UNITS_CHOICES,
        default=1,
        verbose_name="Unit of Age"
    )

    class Meta:
        verbose_name = "Characteristics"
        verbose_name_plural = "Key characteristics"


class FavoriteStar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    star = models.ForeignKey(Star, on_delete=models.CASCADE, related_name="favorited_by")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "star")
