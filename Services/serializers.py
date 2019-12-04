from rest_framework import serializers

from Services.models import Services, Features


class ServicesSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    selected_features = serializers.ListField(write_only=True, allow_empty=False)
    feature_prices = serializers.ListField(write_only=True, allow_empty=False)

    class Meta:
        fields = (
            'name',
            'description',
            'selected_features',
            'feature_prices'
        )
        model = Services

    def to_representation(self, instance):
        try:
            features = [{
                "id": i.feature.id,
                "name": i.feature.name,
                "description": i.feature.description,
                "price": i.pricing
            } for i in instance.servicefeaturepricing_set.all()]

            data = {
                "provider": {
                    "email": instance.provider.email, "first_name": instance.provider.first_name,
                    "last_name": instance.provider.last_name
                },
                "id": instance.id,
                "name": instance.name,
                "description": instance.description,
                "created_at": instance.created_at.strftime("%Y-%m-%d"),
                "features": features
            }
            return data
        except AttributeError:
            return instance


class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = ('id', 'name', 'description')

