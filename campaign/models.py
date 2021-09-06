from django.db import models

class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=False)
    winner = models.BigIntegerField(null=True, default=None)
    finished = models.BooleanField(default=False, null=False)

class Subscriber(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    user_data = models.TextField(null=False, blank=False)
    verified = models.BooleanField(default=False, null=False, blank=False)
    verification_code = models.TextField(null=False, default='')

