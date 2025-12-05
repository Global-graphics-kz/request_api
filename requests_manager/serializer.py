from rest_framework import serializers
from .models import Request

class RequestPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ["status", "priority"]
