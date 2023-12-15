from django.db import models
from uuid import uuid4
import os
from django.core.exceptions import ValidationError

# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=50)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname


class Tag(models.Model):
    name = models.CharField(max_length=30, null=False,unique=True)

    def __str__(self):
        return self.name

class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



def update_filename(instance, filename):
    upload_to = 'uploads'
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join(upload_to, filename)


def validate_file_size(value):
    file_size = value.size
    if file_size > 1000000:
        raise ValidationError("The maximum file size is greater than 1 MB")
    return value


class Picture(models.Model):
    description = models.CharField(max_length=200)
    path = models.ImageField(upload_to=update_filename, validators=[validate_file_size])