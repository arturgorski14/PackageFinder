from django.db import models


class PypiPackage(models.Model):
    description = models.TextField(max_length=512)
