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
    )
]
