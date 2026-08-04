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

]