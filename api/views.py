from django.shortcuts import redirect
import whois
from rest_framework import serializers
from rest_framework.views import APIView
import requests
from .serializers import CreateFormSerializer
# Create your views here.

class ContentAPIView(APIView):
    pass