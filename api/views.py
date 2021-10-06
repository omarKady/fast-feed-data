from django.shortcuts import redirect
import whois
from rest_framework import serializers
from rest_framework.views import APIView
from .serializers import CreateFormSerializer
# Create your views here.

class CreateFeedView(APIView):
    serializer_class = CreateFormSerializer

    # TODO : returns a boolean indicating whether a `url` is registered (exists on the internet)
    @classmethod
    def is_registered(cls, url):
        try:
            domain = whois.whois(url)
        except:
            return False
        else:
            return bool(domain.domain_name)

    # TODO : Take user inputs to check
    def post(self, request):
        serializerform = self.serializer_class(data=self.request.data)
        if not serializerform.is_valid():
            raise serializers.ValidationError("Error : make sure title and url are valid")

        url = serializerform.data['url']
        title = serializerform.data['title']
        print(f'Title : {title} URL : {url}')
        is_valid = self.is_registered(url)
        if is_valid:
            # call function that check if site has rss
            print("Check has rss")
        else:
            raise serializers.ValidationError("Please Enter Valid URL")

        return redirect('create-feed')
