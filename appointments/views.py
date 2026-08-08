from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from datetime import datetime, date, timedelta
from .utils import generate_time_slots

from dashboard.models import Business, Service
from .models import Appointment, Customer
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

            customer, created = Customer.objects.get_or_create(

                business=business,

                phone=appointment.customer_phone,

                defaults={
                    "name": appointment.customer_name,
                    "email": appointment.customer_email,
                }

            )

            # Remember the customer's latest/favorite service
            customer.favorite_service = appointment.service
            customer.save()

            appointment.customer = customer

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
def edit_appointment(request, appointment_id):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        business=business
    )

    if request.method == "POST":

        form = AppointmentForm(
            request.POST,
            instance=appointment,
            business=business
        )

        if form.is_valid():

            form.save()

            return redirect("appointments")

    else:

        form = AppointmentForm(
            instance=appointment,
            business=business
        )

    return render(
        request,
        "appointments/edit_appointment.html",
        {
            "form": form,
            "appointment": appointment,
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


@login_required
def cancel_appointment(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        business__owner=request.user
    )

    appointment.status = "Cancelled"
    appointment.save()

    return redirect("appointments")


@login_required
def complete_appointment(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        business__owner=request.user
    )

    appointment.status = "Completed"
    appointment.save()

    return redirect("appointments")


def business_profile(request, slug):

    business = get_object_or_404(
        Business,
        slug=slug
    )

    return render(
        request,
        "appointments/business_profile.html",
        {
            "business": business,
        }
    )


def available_slots(request, business_id):

    business = get_object_or_404(
        Business,
        id=business_id
    )

    service_id = request.GET.get("service")
    appointment_date = request.GET.get("date")

    if not service_id or not appointment_date:

        return JsonResponse(
            {
                "slots": []
            }
        )

    service = get_object_or_404(
        Service,
        id=service_id
    )

    date_object = datetime.strptime(
        appointment_date,
        "%Y-%m-%d"
    ).date()

    slots = generate_time_slots(
        business,
        service,
        date_object
    )

    return JsonResponse(
        {
            "slots": slots
        }
    )


@login_required
def daily_schedule(request):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    appointments = Appointment.objects.filter(
        business=business,
        appointment_date=date.today()
    ).order_by(
        "appointment_time"
    )

    return render(
        request,
        "appointments/daily_schedule.html",
        {
            "appointments": appointments,
            "today": date.today(),
        }
    )
@login_required
def weekly_schedule(request):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    today = date.today()

    # Get the date requested from the URL
    selected_date = request.GET.get("date")

    if selected_date:

        try:
            current_date = datetime.strptime(
                selected_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            current_date = today

    else:

        current_date = today


    # Find Monday of the selected week
    week_start = current_date - timedelta(
        days=current_date.weekday()
    )

    # Sunday
    week_end = week_start + timedelta(days=6)


    # Get appointments for this week
    appointments = Appointment.objects.filter(
        business=business,
        appointment_date__range=[
            week_start,
            week_end
        ]
    ).order_by(
        "appointment_date",
        "appointment_time"
    )


    # Build each day
    week_days = []

    for i in range(7):

        current_day = week_start + timedelta(
            days=i
        )

        day_appointments = appointments.filter(
            appointment_date=current_day
        )

        week_days.append({
            "date": current_day,
            "appointments": day_appointments,
        })


    # Previous and next week
    previous_week = week_start - timedelta(days=7)

    next_week = week_start + timedelta(days=7)


    return render(
    request,
    "appointments/weekly_schedule.html",
    {
        "week_days": week_days,
        "week_start": week_start,
        "week_end": week_end,
        "previous_week": previous_week,
        "next_week": next_week,
        "today": today,
    }
)