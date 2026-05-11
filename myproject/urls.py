from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)


schema_view = get_schema_view(
    openapi.Info(
        title="NFT API",
        default_version='v1',
        description="NFT Marketplace API",),
    public=True,
    permission_classes=[permissions.AllowAny],)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('art_app.urls')),
    re_path(r'^swagger/$',schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    re_path(r'^redoc/$',schema_view.with_ui('redoc', cache_timeout=0),name='schema-redoc'),
    path('accounts/', include('allauth.urls')),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)