from django.urls import re_path
from . import views

urlpatterns = [
    re_path(
        r'^api/providers/(?P<pk>[0-9]+)$',
        views.get_delete_update_provider,
        name='get_delete_update_provider'
    ),
    re_path(
        r'^api/providers/$',
        views.get_post_providers,
        name='get_post_providers'
    ),
    re_path(
        r'^api/service_areas/(?P<provider_id>[0-9]+)$',
        views.get_post_service_areas,
        name='get_post_service_areas'
    ),
    re_path(
        r'^api/service_areas/(?P<provider_id>[0-9]+)/(?P<pk>[0-9]+)$',
        views.get_delete_update_service_areas,
        name='get_delete_update_service_areas'
    ),
    re_path(
        r'^api/check$',
        views.check_service_areas,
        name='check_service_areas'
    ),
]
