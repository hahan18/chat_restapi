"""chat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from chatapp.views import ThreadCreateDestroyAPIView, ThreadListAPIView, MessageListCreateAPIView, IsReadUpdateAPIView, \
    IsNotReadAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Chat API",
      default_version='v1',
      description="There is a chat api docs",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # -------------------API---------------------------

    # DOCS
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API ENDPOINTS
    path('api/v1/thread/', ThreadCreateDestroyAPIView.as_view(), name='thread'),
    path('api/v1/list/<int:pk>/', ThreadListAPIView.as_view(), name='list'),
    path('ap1/v1/message/', MessageListCreateAPIView.as_view(), name='message_post'),
    path('ap1/v1/message/<int:pk>/', MessageListCreateAPIView.as_view(), name='message_get'),
    path('api/v1/is_read/', IsReadUpdateAPIView.as_view(), name='is_read'),
    path('api/v1/not_read/<int:pk>', IsNotReadAPIView.as_view(), name='is_not_read'),
]
