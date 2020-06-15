from django.db import models

# Create your models here.
class post(models.Model):
    content = models.TextField(max_length=10)
    image = models.ImageField(blank=True,upload_to='image')