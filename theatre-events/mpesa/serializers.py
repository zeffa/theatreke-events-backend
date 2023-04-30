from rest_framework import serializers


class CheckoutSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    amount = serializers.FloatField()
    program_id = serializers.CharField(max_length=50)


class STKItemSerializer(serializers.Serializer):
    Name = serializers.CharField(max_length=50)
    Value = serializers.CharField(max_length=100)


class CallbackMetadataSerializer(serializers.Serializer):
    Item = STKItemSerializer(many=True, read_only=True)


class STKCallbackSerializer(serializers.Serializer):
    MerchantRequestID = serializers.CharField(max_length=255)
    CheckoutRequestID = serializers.CharField(max_length=255)
    ResultCode = serializers.IntegerField(max_value=10)
    ResultDesc = serializers.CharField(max_length=255)
    # CallbackMetadata = CallbackMetadataSerializer()
    CallbackMetadata = serializers.DictField(child=serializers.ListField(child=serializers.DictField()))


class STKBodySerializer(serializers.Serializer):
    stkCallback = STKCallbackSerializer()


class PaymentSuccessSerializer(serializers.Serializer):
    Body = STKBodySerializer()
