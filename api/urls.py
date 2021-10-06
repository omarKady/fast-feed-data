from django.urls import path, include
from .views import CreateFeedView

urlpatterns = [
    path('users/', include('users.urls'), name='users'),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('create-feed/', CreateFeedView.as_view(), name='create-feed'),
    #path('accounts/', include('allauth.urls')),
]
