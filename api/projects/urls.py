"""projets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter
from lvao.views import CSVFileUploadView, CSVFileProcessViewSet, download_csv


router = DefaultRouter()
router.register(r'csv-files', CSVFileProcessViewSet)
apiUrls = [
    re_path(r"^uploadcsv/?", CSVFileUploadView.as_view()),
    path('download-csv/', download_csv, name='download_csv'),
]

urlpatterns = [
    # viewset
    path("v1/", include(router.urls)),
    # view
    path("v1/", include((apiUrls, "api"), namespace="v1")),
    # admin
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    # urlpatterns += static(
    #     settings.STATIC_URL,
    #     document_root=settings.STATIC_ROOT
    # )
