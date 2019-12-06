from django.db import models
from Services.models import ServiceFeaturePricing


class Client(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()


class ClientSubscriptions(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # this field to be a list of ServiceFeaturePricing table ids
    subscribed_list = models.TextField(blank=True, null=True)
    sub_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
