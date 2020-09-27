from django.db import models

# Create your models here.
class Quiz(models.Model):
    question = models.CharField(max_length=200, null=True)
    option1 = models.CharField(max_length=100, null=True)
    option2 = models.CharField(max_length=100, null=True)
    option3 = models.CharField(max_length=100, null=True)
    correctAns = models.CharField(max_length=100, null=True)
    tag = models.CharField(max_length=100, null=True)