from django.db import models
from Services.models import ServiceFeaturePricing


class Client(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()


class ClientSubscriptions(models.Model):
    service_feature = models.ForeignKey(ServiceFeaturePricing, on_delete=models.CASCADE)
    sub_date = models.DateTimeField(auto_now_add=True)
