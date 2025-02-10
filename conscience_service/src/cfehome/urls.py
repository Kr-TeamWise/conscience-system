"""
URL configuration for cfehome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from ninja import NinjaAPI
from api.docs import MixedDocs
from user.api import router as user_router
from django.contrib.admin.views.decorators import staff_member_required

base_api = NinjaAPI(
    title="Mansung API",
    version="0.1.0",
    docs_url="/<engine>/",
    docs_decorator=staff_member_required,
    docs=MixedDocs(),
)


@base_api.get("", include_in_schema=False)
def health_check_handler(request):
    return {"ping": "pong"}


base_api.add_router("v1/auth", user_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", base_api.urls),
]
