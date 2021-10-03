from rest_framework import serializers
from .models import CustomUser

class ListUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'username',)
