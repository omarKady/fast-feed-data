from .models import Feed
from django.db.models import fields
from rest_framework import serializers

# List feed serializer
class FeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feed
        fields = ('title', 'url',)

# Create feed form serializer
class CreateFormSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=250)
    url = serializers.CharField()
