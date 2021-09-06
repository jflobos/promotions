from django.db import models
from django.db.models.fields import BigAutoField

class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=False)

class Subscriber(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    user_data = models.TextField(null=False, blank=False)
    verified = models.BooleanField(default=False, null=False, blank=False)
    verification_code = models.TextField(null=False, default='')

