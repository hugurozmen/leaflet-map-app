from django.contrib.gis.db import models

# Create your models here.


class Places(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    point = models.PointField()
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.type}'