from rest_framework import serializers
from users.models import User


class UserDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email"]
