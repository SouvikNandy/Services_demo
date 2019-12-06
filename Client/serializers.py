from rest_framework import serializers

from Client import validators
from Client.models import ClientSubscriptions
from Services.models import ServiceFeaturePricing


class ClientSubscriptionSerializer(serializers.ModelSerializer):
    service = serializers.JSONField(write_only=True, required=True)

    class Meta:
        model = ClientSubscriptions
        fields = ('id', 'service')

    @staticmethod
    def validate_service(attrs):
        data = validators.validate_subscription_json(attrs)
        return data

    def to_representation(self, instance):
        try:
            # subscribed_list is currently stored as string
            sub_map = instance.subscribed_list.split(",")
            subscribed_index = dict()
            subscribed_services = list()
            for i in sub_map:
                obj = ServiceFeaturePricing.objects.get(id=i)

                feature_obj = obj.feature
                feature = [{
                    "id": feature_obj.id,
                    "name": feature_obj.name,
                    "description": feature_obj.description,
                    "price": obj.pricing
                }]

                if obj.service_id in subscribed_index:
                    index = subscribed_index[obj.service_id]
                    subscribed_services[index]["features"].append(feature)

                else:
                    service_obj = obj.service
                    subscribed_services.append({
                        # "provider": {
                        #     "email": service_obj.provider.email, "first_name": service_obj.provider.first_name,
                        #     "last_name": service_obj.provider.last_name
                        # },
                        "id": service_obj.id,
                        "name": service_obj.name,
                        "description": service_obj.description,
                        "features": feature
                    })
                    # store the index of service in subscribed_services
                    index = len(subscribed_services) - 1
                    subscribed_index[obj.service_id] = index
            data = {
                "id": instance.id,
                "subscription_date": instance.sub_date.strftime("%Y-%m-%d"),
                "is_active": instance.is_active,
                "services": subscribed_services
            }
            return data
        except:
            return instance
