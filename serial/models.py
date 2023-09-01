from django.db import models
from PIL import Image  # Import Pillow's Image module

from django.db import models

from account.models import User


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class TVShow(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    num_seasons = models.PositiveIntegerField()
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1)
    preview_image = models.ImageField(upload_to='tvshow_previews/', null=True, blank=True)
    preview_video = models.FileField(upload_to='tvshow_videos/', null=True, blank=True)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title


class Episode(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.FileField(upload_to='episodes/')
    episode_number = models.PositiveIntegerField()
    tvshow = models.ForeignKey(TVShow, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tvshow.title} - Episode {self.episode_number}: {self.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tvshow = models.ForeignKey(TVShow, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.tvshow.title}"
