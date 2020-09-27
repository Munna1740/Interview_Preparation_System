from django.db import models

# Create your models here.
class JobPost(models.Model):
    jobTitle = models.CharField(max_length=150, null=True)
    shortDescription = models.CharField(max_length=1000, null=True)
    shortRequirement = models.CharField(max_length=1000, null=True)
    link = models.CharField(max_length=150, null=True)