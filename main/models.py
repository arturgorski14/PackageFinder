from django.db import models


class PypiPackage(models.Model):
    description = models.CharField(max_length=512)
