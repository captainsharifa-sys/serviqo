from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from dashboard.models import Business
from .models import Appointment
from .forms import AppointmentForm


def book_appointment(request, business_id):

    business = get_object_or_404(
        Business,
        id=business_id
    )

    if request.method == "POST":

        form = AppointmentForm(
            request.POST,
            business=business
        )

        if form.is_valid():

            appointment = form.save(commit=False)

            appointment.business = business

            appointment.save()

            return redirect(
                "book_appointment",
                business_id=business.id
            )

    else:

        form = AppointmentForm(
            business=business
        )

    return render(
        request,
        "appointments/book.html",
        {
            "business": business,
            "form": form,
        }
    )


@login_required
def appointments_list(request):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    appointments = Appointment.objects.filter(
        business=business
    ).order_by(
        "appointment_date",
        "appointment_time"
    )

    return render(
        request,
        "appointments/appointments.html",
        {
            "appointments": appointments
        }
    )
@login_required
def confirm_appointment(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        business__owner=request.user
    )

    appointment.status = "Confirmed"
    appointment.save()

    return redirect("appointments")