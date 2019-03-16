from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class abc_model(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.CharField(max_length=55)
    description = models.TextField(max_length=55)
