from django.db import models

class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=False)

class Subscriber(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    user_data = models.TextField(null=False, blank=False)
