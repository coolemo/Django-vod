"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from rest_framework.documentation import include_docs_urls
import admin_resumable
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token

from mysite.upload import upload_image

admin.site.site_header = '视频点播管理系统'
urlpatterns = [
    # url(r'^docs/', include('rest_framework_docs.urls')),
    # url(r'^', include('drf_autodocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin_resumable/', include('admin_resumable.urls')),

    # url(r'^polls/',include('polls.urls')),
    # url(r'^tools/',include('tools.urls')),
    url(r'^api/auth/token/', obtain_jwt_token),
    url(r'^tv/api/', include("epg.api.urls", namespace='tv-api')),
    url(r'^vod/api/', include("vodmanagement.api.urls", namespace='vod-api')),
    url(r'', include('vodmanagement.urls', namespace='vod')),
    # url(r'^progressbarupload/', include('progressbarupload.urls')),

    # url(r'^filer/',include('filer.urls')),
    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^accounts/', include('allauth.urls')),
    url(r'^uploads/(?P<dir_name>[^/]+)$', upload_image, name='upload_image')
]
# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
