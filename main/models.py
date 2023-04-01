from django.db import models


class PypiPackage(models.Model):
    # author_name = models.CharField(max_length=64)
    # author_email = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    # maintainer_data = models.CharField(max_length=192)
    title = models.CharField(max_length=128)
    version = models.CharField(max_length=16)
    # keywords - add later
