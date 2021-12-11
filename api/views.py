from api.models import Feed, FollowedItems
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from .tasks import get_feed_to_check
from .serializers import FeedSerializer, FollowedItemSerializer
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

# TODO : List all feeds of user (requester) 
@api_view(['GET'])
def get_user_feeds(request):
    if request.method == 'GET':
        requester = request.user
        #feeds = Feed.objects.filter(owner=requester)
        feeds = Feed.objects.raw('SELECT id,title,owner_id FROM api_feed WHERE owner_id=%s',[request.user.id])
        print('FEEDS: ', feeds.query)
        serializer = FeedSerializer(feeds, many=True)
        return Response(serializer.data)

# TODO : User can follow feed item
@api_view(['POST'])
def user_follow_feed(requset, pk):
    try:
        feed = Feed.objects.get(id=pk)
    except:
        raise Http404

    if requset.method == 'POST':
        follower = requset.user.id
        feed = Feed.objects.get(id=pk).id
        datas = {'follower':follower, 'feed_item':feed}
        serializer = FollowedItemSerializer(data=datas)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO : User unfollow feed item
@api_view(['DELETE'])
def user_unfollow_feed(request, pk):
    try:
        feed = Feed.objects.get(id=pk)
        user = request.user
        followed_item = FollowedItems.objects.get(feed_item_id=pk, follower_id=user.id)
    except:
        raise Http404
    
    if request.method == 'DELETE':
        followed_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
