from django.urls import path, include

from ads.views import AdViewSet, CommentViewSet
from rest_framework import routers

ads_router = routers.SimpleRouter()
ads_router.register('ads', AdViewSet)
ads_router.register('ads/(?P<ad_id>[^/.]+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(ads_router.urls)),
]
