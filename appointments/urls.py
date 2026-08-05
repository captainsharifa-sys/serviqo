from django.urls import path
from . import views


urlpatterns = [

    path(
        "book/<int:business_id>/",
        views.book_appointment,
        name="book_appointment",
    ),

    path(
        "appointments/",
        views.appointments_list,
        name="appointments",
    ),

    path(
        "appointments/<int:appointment_id>/confirm/",
        views.confirm_appointment,
        name="confirm_appointment",
    ),

    path(
        "appointments/<int:appointment_id>/cancel/",
        views.cancel_appointment,
        name="cancel_appointment",
    ),

    path(
        "appointments/<int:appointment_id>/complete/",
        views.complete_appointment,
        name="complete_appointment",
    ),

    path(
    "business/<slug:slug>/",
    views.business_profile,
    name="business_profile",
),
path(
    "available-slots/<int:business_id>/",
    views.available_slots,
    name="available_slots",
),

]