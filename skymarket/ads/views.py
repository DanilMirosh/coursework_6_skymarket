from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets
from drf_spectacular import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from ads.models import Ad, Comment
from ads.filters import AdsFilter
from ads.permissions import IsOwnerOrStaff

from ads.serializers import AdListSerializer, AdDetailSerializer, CommentViewSet, CommentSerializer


class AdPagination(pagination.PageNumberPagination):
    page_size = 4
    page_query_param = 'page'


@extend_schema_view(
    list=extend_schema(summary='Список всех объявлений'),
    create=extend_schema(summary='Создание объявления'),
    retrieve=extend_schema(summary='Подробно об объявлении'),
    partial_update=extend_schema(summary='Изменить объявление'),
    destroy=extend_schema(summary='Удалить объявление'),
)
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().select_related('author')
    pagination_class = AdPagination
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = (DjangoFilterBackend)
    filter_class = AdsFilter

    serializers = {"list": AdListSerializer, }
    default_serializer = AdDetailSerializer

    permissions = {
        "create": [IsAuthenticated()],
        "retrieve": [IsAuthenticated()],
        "update": [IsAuthenticated(), IsOwnerOrStaff()],
        "partial_update": [IsAuthenticated(), IsOwnerOrStaff()],
        "destroy": [IsAuthenticated(), IsOwnerOrStaff()],
    }

    default_permissions = [AllowAny()]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permissions)

    # Переопределяем метод для добавления в serializer поля автор
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(summary='Мои объявления', response=AdListSerializer)
    @action(detail=True, methods=['get'], permissions_classes=[IsOwnerOrStaff], url_path="me")
    def get_ads_by_user(self, request):
        """
        Get listing of ads from the current_user
        """
        ads = Ad.objects.filter(author_id=self.request.user.pk)
        paginator = AdPagination()

        page_obj = paginator.paginate_queryset(queryset=ads, request=request)

        return paginator.get_paginated_response(AdListSerializer(page_obj, many=True).data)

    @extend_schema_view(
        list=extend_schema(summary='Список отзывов'),
        create=extend_schema(summary='Оставить отзыв'),
        retrieve=extend_schema(summary='Получить отзыв по ID'),
        partial_update=extend_schema(summary='Изменить отзыв'),
        destroy=extend_schema(summary='Удалить отзыв'),
    )
    class CommentViewSet(viewsets.ModelViewSet):
        queryset = Comment.objects.all()
        permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        serializer_class = CommentSerializer
        http_method_names = ["get", "post", "patch", "delete"]

        def get_queryset(self):
            return self.queryset.filter(ad=self.kwargs['ap_pk']).select_related('author')

        def perform_create(self, serializer):
            serializer.save(author=self.request.user, ad_id=self.kwargs['ap_pk'])
