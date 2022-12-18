from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/redoc-tasks/", include("redoc.urls")),
    path("api/users/", include("users.urls")),
    path("api/ads/", include("ads.urls")),

    # URLs аутентификации по JWT.
    path("api/token/", TokenObtainPairView.as_view(), name="jwt-create"),
    path("api/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("api/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = [
                      # URLs документации.
                      path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                      path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema')),

                      # URLs Debug Toolbar
                      path('__debug__/', include('debug_toolbar.urls')),
                  ] + urlpatterns
