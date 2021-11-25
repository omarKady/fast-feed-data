from api.models import Feed
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from .tasks import get_feed_to_check
from .serializers import FeedSerializer
# Create your views here.

# TODO : get detail of feed object, delete or update
@api_view(['GET', 'DELETE', 'PUT'])
def feed_detail(request, pk):
    try:
        feed = Feed.objects.get(pk=pk)
    except:
        raise Http404

    if request.method == 'GET':
        seriallizer = FeedSerializer(feed)
        return Response(seriallizer.data)

    elif request.method == 'DELETE':
        feed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        seriallizer = FeedSerializer(feed, data=request.data)
        if seriallizer.is_valid():
            seriallizer.save()
            return Response(seriallizer.data)
        return Response(seriallizer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO : get list of feeds or create new resource
@api_view(['GET', 'POST'])
def get_feeds_list(request):
    if request.method == 'GET':
        feeds = Feed.objects.all()
        serializer = FeedSerializer(feeds, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FeedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            feed_id = serializer.data['id']
            #get_feed_to_check.apply_async((feed_id,), countdown=15)
            get_feed_to_check.delay(feed_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
