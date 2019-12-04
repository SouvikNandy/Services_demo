from rest_framework import serializers

from Client.models import ClientSubscriptions


class ClientSubscriptionSerializer(serializers.ModelSerializer):
    service = serializers.JSONField(write_only=True, required=True)

    class Meta:
        model = ClientSubscriptions
        fields = ('id', 'service')

    def to_representation(self, instance):
        try:
            service_list = list()
            service_id_collection = dict()
            data = {}
            for i in instance:
                srv = i.service_feature.service
                ft = i.service_feature.feature
                ft_data = {
                    "name": ft.name,
                    "description": ft.description,
                    "price": i.service_feature.pricing,
                    "subscription_date": i.sub_date.strftime("%Y-%m-%d"),
                }
                if srv.id not in service_id_collection:
                    # service_id_collection.add(service_id)
                    service_list.append({
                        "id": srv.id,
                        "provider": srv.provider.email,
                        "features": [ft_data]
                    })
                    service_id_collection[srv.id] = len(service_list) - 1
                else:
                    index = service_id_collection[srv.id]
                    service_list[index]["features"].append(ft_data)
                # add features and prices

                data = {
                    "services": service_list,
                }
            return data
        except:
            return instance
