from django.db import models


class ServiceProvider(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()


class Services(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    # convenience_charges = models.FloatField(default=500)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class Features(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=True)


class ServiceFeaturePricing(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    feature = models.ForeignKey(Features, on_delete=models.CASCADE)
    pricing = models.FloatField()
    is_active = models.BooleanField(default=True)

