"""sims URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from sims.api.urls import urlpatterns as api_urlpatterns
from django.urls import include, re_path
from sims.api import views

urlpatterns = [
    path("server/admin/", admin.site.urls),
    re_path(r"^server/api/", include(api_urlpatterns)),
    re_path(r"^server/api-auth/", include("rest_framework.urls")),
    re_path(r"^server/api/logout/$", views.logout_view, name="logout"),
    re_path(r"^server/api/get_user/$", views.get_user, name="get_user"),
    path('server/social/', include('social_django.urls', namespace='social'))
]
