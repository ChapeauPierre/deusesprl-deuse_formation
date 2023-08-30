import user.models

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user.models.User
        fields = ['id', 'email']
