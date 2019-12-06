from rest_framework import serializers

from Services.models import ServiceFeaturePricing


def validate_service(service, subscription_options):
    if not service[1]:
        raise serializers.ValidationError("Features must not be blank for service {}".format(service[0]))

    for ft in service[1]:
        try:
            obj = ServiceFeaturePricing.objects.get(service_id=service[0], feature_id=ft)
            subscription_options.append(obj.id)
        except ServiceFeaturePricing.DoesNotExist:
            raise serializers.ValidationError(
                "Please provide valid service/features choice. Service={}, Feature={}".format(service[0], ft))
    return subscription_options


def validate_subscription_json(data):
    subscription_options = list()
    for d in data.items():
        validate_service(d, subscription_options)
    return subscription_options
