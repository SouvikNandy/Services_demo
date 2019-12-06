from django.db.models import Sum
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

        user_subs = self.client_subscription_model.objects.filter(client_id=client_id)
        serialized_data = self.serializer_class(user_subs, many=True)
        return Response({"status": True,
                         "message": "Available Subscription",
                         "data": serialized_data.data},
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
        subscription_services = clean_data["service"]

        if 'payable' in request.query_params and request.query_params["payable"] in ['True', 'true']:
            calculate_payable = True
        else:
            calculate_payable = False
        print(subscription_services)
        if calculate_payable:
            price = self.calculate_tariff(subscription_services)
            return Response({"status": True,
                             "message": "Price to be paid",
                             "data": price},
                            status=status.HTTP_200_OK)
        else:
            self.client_subscription_model.objects.create(
                client_id=client_id,
                subscribed_list=','.join([str(elem) for elem in subscription_services]),
                is_active=True
            )
            return Response({"status": True, "message": "new subscription created", "data": None},
                            status=status.HTTP_200_OK)

    @staticmethod
    def calculate_tariff(data):
        price = 0
        convenience_charges = 500

        query = ServiceFeaturePricing.objects.filter(id__in=data)
        price += query.aggregate(sum_amt=Sum('pricing'))['sum_amt']
        return price + convenience_charges
