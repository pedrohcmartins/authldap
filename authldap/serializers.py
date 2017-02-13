from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_pass = serializers.CharField(required=True)
    new_pass = serializers.CharField(required=True)
