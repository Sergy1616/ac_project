from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from .validators import validate_file_size


def upload_photo(instance, filename):
    return f"users/{instance.username}/{filename}"


class Profile(AbstractUser):
    photo = models.ImageField(
        upload_to=upload_photo, blank=True, validators=[validate_file_size]
    )
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'username': self.username})

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.email = self.email.lower()
        super(Profile, self).save(*args, **kwargs)
