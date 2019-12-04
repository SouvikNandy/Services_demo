from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from Services.models import Services, ServiceFeaturePricing, Features
from Services import serializers


class ServicesAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.ServicesSerializer

    def get(self, request):
        """
        Get all available services including Features etc.
        :param request:
        :return:
        """
        available_services = Services.objects.prefetch_related('servicefeaturepricing_set').all()
        if not available_services:
            return Response({"status": True, "message": "Successful request", "data": {}},
                            status=status.HTTP_200_OK)
        serialized_data = self.serializer_class(available_services, many=True)

        return Response({"status": True,
                         "message": "Available services and features with pricing",
                         "data": serialized_data.data},
                        status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create new Service
        :param request:
        :return:
        """
        serializer = self.serializer_class(data=request.data)
        print("data sent to serializer")
        if not serializer.is_valid():
            return Response({"status": False, "message": serializer.errors, "data": None},
                            status=status.HTTP_400_BAD_REQUEST)
        cleaned_data = serializer.data
        obj = Services.objects.create(provider_id=1, name=cleaned_data["name"], description=cleaned_data["description"])
        # bulk create on ServiceFeaturePricing
        rows_to_upload = list()
        for idx, data in enumerate(cleaned_data["selected_features"]):
            rows_to_upload.append(
                ServiceFeaturePricing(service_id=obj.id, feature_id=data, pricing=cleaned_data["feature_prices"][idx])
            )
        ServiceFeaturePricing.objects.bulk_create(rows_to_upload)
        return Response({"status": True, "message": "new service created", "data": None},
                        status=status.HTTP_200_OK)


class FeaturesAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.FeaturesSerializer
    features_model = Features

    def get(self, request):
        """
        get all available features
        :param request:
        :return:
        """
        available_features = self.features_model.objects.all()
        serialized_data = self.serializer_class(available_features, many=True)
        return Response({"status": True, "message": "Available Features", "data": serialized_data.data},
                        status=status.HTTP_200_OK)
