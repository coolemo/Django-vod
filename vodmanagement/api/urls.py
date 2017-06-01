from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^$', VodListAPIView.as_view(), name='list'),
    # url(r'^create/$', PostCreateAPIView.as_view(), name='create'),
    url(r'^(?P<id>[\w-]+)/$', VodDetailAPIView.as_view(), name='detail'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateAPIView.as_view(), name='update'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', PostDeleteAPIView.as_view(), name='delete'),
]
