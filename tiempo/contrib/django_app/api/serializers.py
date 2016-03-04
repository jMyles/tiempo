from rest_framework import serializers


class JobSerializer(serializers.Serializer):

    status = serializers.CharField(max_length=200)
