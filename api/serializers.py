from django.core.checks.messages import Error
from django.db import models
from django.db.models import fields
from rest_framework import serializers
import requests
from .models import Feed, FollowedItems

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


class FollowedItemSerializer(serializers.ModelSerializer):
    
    def validate(self, data):
        follower = data['follower'].id
        feed = data['feed_item']
        feed_owner = Feed.objects.get(id=feed.pk).owner.id
        old_item = FollowedItems.objects.filter(feed_item_id=feed.pk, follower_id=follower)
        if old_item:
            raise serializers.ValidationError({'feed_item_id':['User can not follow item more than one time',]})
        if feed_owner == follower:
            raise serializers.ValidationError({'follower_id':['Owner can not follow his feed']})
        else:
            return data

    class Meta:
        model = FollowedItems
        fields = '__all__'
