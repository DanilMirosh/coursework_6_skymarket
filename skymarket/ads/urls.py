from os.path import basename

from django.urls import include, path
from rest_framework import routers

from ads.views import AdViewSet, CommentViewSet

ads_router = routers.SimpleRouter()
ads_router.register('', AdViewSet)
comments_router = routers.NestedSimpleRouter(ads_router, '', lookup='ad')
comments_router.register('comments', CommentViewSet, basename='ad_comments')

urlpatterns = [
    path("", include(ads_router.urls)),
    path("", include(comments_router.urls)),
]
