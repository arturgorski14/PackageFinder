from django.db import models


class Package(models.Model):
    description = models.TextField(max_length=512)
