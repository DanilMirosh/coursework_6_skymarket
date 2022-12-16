from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad
from ads.serializers import AdSerializer, AdListSerializer, AdRetrieveSerializer, AdCreateSerializer
from ads.permissions import UserPermissions


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer

    serializer_action_classes = {
        'list': AdListSerializer,
        'retrieve': AdRetrieveSerializer,
        'create': AdCreateSerializer,
        'update': AdCreateSerializer,
    }
    permission_classes = (UserPermissions,)

    @action(detail=False, methods=['get'], url_path=r'me', serializer_class=AdListSerializer)
    def user_ads(self, request, *args, **kwargs):
        current_user = self.request.user
        user_ads = Ad.objects.filter(author=current_user)
        page = self.paginate_queryset(user_ads)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
