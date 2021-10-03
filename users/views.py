from django.db import models
from .models import CustomUser
from .serializers import ListUsersSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

class UsersListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ListUsersSerializer
    permission_classes = [IsAdminUser]
