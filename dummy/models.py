from django.db import models


class FirstDummy(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='dummy/images')

    def __str__(self):
        return self.name


class SecondDummy(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='dummy/files')

    def __str__(self):
        return self.name
