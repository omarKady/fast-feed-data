from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Feed

# List feed serializer

class FeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feed
        fields = '__all__'
