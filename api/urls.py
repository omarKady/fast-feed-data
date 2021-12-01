from django.urls import path, include
from .views import feed_detail, get_feeds_list, get_user_feeds

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('feeds/<int:pk>/', feed_detail, name='feed_detail'),
    path('feeds/', get_feeds_list, name='get_feeds_list'),
    path('feeds/my/', get_user_feeds, name='get_user_feeds'),
]
