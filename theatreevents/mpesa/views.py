import json

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers
from .helpers import format_phone_number, write_json_to_file
from .lipa_na_mpesa import LipaNaMpesa
from .models import PaymentTransaction
from .serializers import PaymentSuccessSerializer


class PaymentViewSet(viewsets.ViewSet):
    mpesa = LipaNaMpesa()

    @action(detail=False, methods=['POST'], url_path='stk-push')
    def stk_push(self, request):
        data = request.data
        serializer = serializers.CheckoutSerializer(data=data)
        if not serializer.is_valid():
            return Response(data=serializer.errors)
        amount = serializer.validated_data['amount']
        raw_number = serializer.validated_data['phone_number']
        formatted_phone = format_phone_number(raw_number)
        stk_response = self.mpesa.stk_push(amount=amount, phone_number=formatted_phone)
        return Response(data=stk_response.json(), status=stk_response.status_code)

    @csrf_exempt
    @action(detail=False, methods=['POST'], url_path='transactions', permission_classes=[permissions.AllowAny])
    def confirmation_url(self, request):
        write_json_to_file(json, request.data, 'request.json')
        data = json.loads(json.dumps(request.data))
        write_json_to_file(json, data, 'request_dump.json')
        serializer = PaymentSuccessSerializer(data=data)
        if not serializer.is_valid():
            return
        body = serializer.validated_data['Body']
        stk_callback = body["stkCallback"]
        merchant_request_id = stk_callback["MerchantRequestID"]
        checkout_request_id = stk_callback["CheckoutRequestID"]
        result_code = stk_callback["ResultCode"]
        result_desc = stk_callback["ResultDesc"]
        callback_metadata = stk_callback["CallbackMetadata"]
        item = callback_metadata["Item"]
        amount = item[0]["Value"]
        receipt_number = item[1]["Value"]
        transaction_date = item[2]["Value"]
        phone_number = item[3]["Value"]

        transaction = PaymentTransaction(
            merchant_request_id=merchant_request_id,
            checkout_request_id=checkout_request_id,
            phone_number=phone_number,
            amount=amount,
            receipt_number=receipt_number,
            result_code=result_code,
            result_description=result_desc,
            is_finished=True,
            is_successful=True
        )
        transaction.set_transaction_date(str(transaction_date))
        transaction.save()
        return Response(data={"ResultCode": 0, "ResultDesc": "Payment Completed successfully"})

    @action(detail=False, methods=['POST'])
    def validation_url(self, request):
        pass

    @action(detail=False, methods=['GET'], url_path='register-callbacks', permission_classes=[permissions.AllowAny])
    def register_callbacks(self, request):
        response = self.mpesa.register_callbacks()
        return Response(data=response.json(), status=response.status_code)
