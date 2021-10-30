from api.models import Feed
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from .serializers import FeedSerializer
# Create your views here.

# TODO : get detail of feed object or not found error
@api_view(['GET'])
def feed_detail(request, pk):
    try:
        feed = Feed.objects.get(pk=pk)
        seriallizer = FeedSerializer(feed)
        return Response(seriallizer.data)
    except:
        raise Http404


# TODO : get list of feeds
@api_view(['GET'])
def get_feeds_list(request):
    feeds = Feed.objects.all()
    serializer = FeedSerializer(feeds, many=True)
    return Response(serializer.data)
