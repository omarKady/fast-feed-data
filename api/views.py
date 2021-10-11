from django.shortcuts import redirect
import whois
from rest_framework import serializers
from rest_framework.views import APIView
import requests
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

    # TODO : get full url site
    @classmethod
    def get_full_site_url(self, url):
        domain = whois.whois(url)
        site_name = domain.domain_name
        if isinstance(site_name, str):
            full_site_url = 'http://' + site_name
        elif isinstance(site_name, list):
            full_site_url = 'http://' + site_name[0]
        site_url = requests.get(full_site_url).url
        return site_url

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
            # get full site url
            full_url = self.get_full_site_url(url)
            print("Full url : ", full_url)
        else:
            raise serializers.ValidationError("Please Enter Valid URL")

        return redirect('create-feed')
