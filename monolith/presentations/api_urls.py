from django.urls import path

from .api_views import (api_approve_presentation,
                        api_list_presentations,
                        api_reject_presentation,
                        api_show_presentation)

urlpatterns = [
    path(
        "presentations/<int:pk>/approval/",
        api_approve_presentation,
        name="api-approve_presentation",
    ),
    path(
        "presentations/<int:pk>/rejection/",
        api_reject_presentation,
        name="api_reject_presentation",
    ),
    path(
        "conferences/<int:conference_id>/presentations/",
        api_list_presentations,
        name="api_list_presentations",
    ),
    path(
        "presentations/<int:pk>/",
        api_show_presentation,
        name="api_show_presentation",
    ),
]
