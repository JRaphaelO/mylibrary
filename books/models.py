import uuid
from django.db import models

# Create your models here.
class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year_published = models.IntegerField()

    def __str__(self):
        return self.title

class BookData(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    description = models.TextField()
    info_link = models.URLField()
    image_link = models.URLField()

    def __str__(self):
        return self.title