from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from Client import serializers
from Client.models import ClientSubscriptions
from Services.models import ServiceFeaturePricing


class ClientSubscriptionAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.ClientSubscriptionSerializer
    client_subscription_model = ClientSubscriptions

    def get(self, request):
        """
        return client's available subscription
        :param request:
        :return:
        """
        client_id = 1
        if 'payable' in request.query_params and request.query_params["payable"] in ['True', 'true']:
            calculate_payable = True
        else:
            calculate_payable = False

        user_subs = self.client_subscription_model.objects.select_related('service_feature').filter(client_id=client_id)
        if calculate_payable:
            price = self.calculate_tariff(user_subs)
            return Response({"status": True,
                             "message": "Price to be paid",
                             "data": price},
                            status=status.HTTP_200_OK)

        serialized_data = self.serializer_class(user_subs)
        return Response({"status": True,
                         "message": "Available Subscription",
                         "data": serialized_data.data["services"]},
                        status=status.HTTP_200_OK)

    def post(self, request):
        """
        subscribe to a service, with optional features, prices
        :param request:
        :return:
        """
        client_id = 1
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": serializer.errors, "data": None},
                            status=status.HTTP_400_BAD_REQUEST)
        clean_data = serializer.data
        services = clean_data["service"]
        subs_package = list()
        for srv in services:
            if not services[srv]:
                return Response({"status": False,
                                 "message": "Please provide features for service {}".format(srv),
                                 "data": None}, status=status.HTTP_400_BAD_REQUEST)
            for ft in services[srv]:
                try:
                    service_package = ServiceFeaturePricing.objects.get(service_id=srv, feature_id=ft)
                except ServiceFeaturePricing.DoesNotExist:
                    return Response({
                        "status": False,
                        "message": "Please provide valid service/features choice. Service={}, Feature={}".format(
                            srv, ft),
                        "data": None}, status=status.HTTP_400_BAD_REQUEST)
                subs_package.append(
                    self.client_subscription_model(client_id=client_id,
                                                   service_feature_id=service_package.id)
                )
        # bulk create records for ClientSubscriptions
        self.client_subscription_model.objects.bulk_create(subs_package)
        return Response({"status": True, "message": "new subscription created", "data": None},
                        status=status.HTTP_200_OK)

    @staticmethod
    def calculate_tariff(instance):
        price = 0
        convenience_charges = 500
        for i in instance:
            price += i.service_feature.pricing
        return price + convenience_charges
