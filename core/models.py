from django.db import models
import uuid

# Create your models here.
class Movie(models.Model):
    GENRE_CHOICES = [
        ('action','Action'),
        ('comedy','Comedy'),
        ('drama','Drama'),
        ('horror','Horror'),
        ('romance','Romance'),
        ('science_fiction','Science Fiction'),
        ('fantasy','Fantasy'),
    ]
    
    uu_id = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    length = models.PositiveIntegerField()
    image_card = models.ImageField(upload_to='movies_image/')
    image_cover = models.ImageField(upload_to='movies_image/')
    video = models.FileField(upload_to='movies_image/')
    movie_views = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.title
