from django.urls import path
from . import views

urlpatterns = [

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "create-business/",
        views.create_business,
        name="create_business",
    ),

    path(
        "services/",
        views.services,
        name="services",
    ),

    path(
        "services/<int:service_id>/edit/",
        views.edit_service,
        name="edit_service",
    ),

    path(
    "working-hours/<int:hour_id>/edit/",
    views.edit_working_hour,
    name="edit_working_hour",
),

    path(
        "working-hours/",
        views.working_hours,
        name="working_hours",
    ),

path(
    "services/<int:service_id>/delete/",
    views.delete_service,
    name="delete_service",
),
path(
    "working-hours/<int:hour_id>/delete/",
    views.delete_working_hour,
    name="delete_working_hour",
),
]