from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.shortcuts import redirect
from django.conf.urls.static import static
from config import settings


def redirect_login(request):
    return redirect("login")


schema_view = get_schema_view(
    openapi.Info(
        title="Referral API",
        default_version='v1',
        description="Реферальная система с авторизацией по телефону и инвайт-кодами.",
        contact=openapi.Contact(email="your_email@example.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[]
)

urlpatterns = [
    path('api/', include('users.urls_api')),
    path('', include('users.urls_web')),
    path('admin/', admin.site.urls),

    # Документация:
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
urlpatterns += [
    path('accounts/login/', redirect_login),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
