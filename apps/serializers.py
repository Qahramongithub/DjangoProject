from rest_framework import serializers


class HikvisionAccessSerializer(serializers.Serializer):
    fullname = serializers.CharField(required=True)
    date = serializers.DateTimeField(required=True)
    status = serializers.CharField(required=False)  # "checkIn" yoki "checkOut"
