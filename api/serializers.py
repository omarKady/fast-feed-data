from rest_framework import serializers
import requests
from .models import Feed

# List feed serializer

class FeedSerializer(serializers.ModelSerializer):

    def validate(self, data):
        url = data['url']
        try:
            domain = requests.get(url)
            return data
        except:
            raise serializers.ValidationError({'url': ["URL is not valid domain name",]})
    
    class Meta:
        model = Feed
        fields = '__all__'
