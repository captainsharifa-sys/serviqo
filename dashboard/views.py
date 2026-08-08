from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from appointments.models import Appointment,Customer

from .forms import BusinessForm
from .service_forms import ServiceForm
from .working_forms import WorkingHourForm
from .models import Business, Service, WorkingHour,Staff
from .staff_forms import StaffForm


@login_required
def dashboard(request):

    business = Business.objects.filter(
        owner=request.user
    ).first()

    total_services = 0
    total_working_hours = 0
    total_appointments = 0
    today_appointments = []

    if business:

        total_services = business.services.count()

        total_working_hours = business.working_hours.count()

        total_appointments = Appointment.objects.filter(
            business=business
        ).count()

        today_appointments = Appointment.objects.filter(
            business=business,
            appointment_date=date.today()
        ).order_by("appointment_time")

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "business": business,
            "total_services": total_services,
            "total_working_hours": total_working_hours,
            "total_appointments": total_appointments,
            "today_appointments": today_appointments,
        }
    )


@login_required
def create_business(request):

    if request.method == "POST":

        form = BusinessForm(request.POST)

        if form.is_valid():

            if Business.objects.filter(owner=request.user).exists():
                return redirect("dashboard")

            business = form.save(commit=False)
            business.owner = request.user
            business.save()

            return redirect("dashboard")

    else:

        form = BusinessForm()

    return render(
        request,
        "dashboard/create_business.html",
        {
            "form": form
        }
    )


@login_required
def services(request):

    business = Business.objects.get(owner=request.user)

    if request.method == "POST":

        form = ServiceForm(request.POST)

        if form.is_valid():

            service = form.save(commit=False)
            service.business = business
            service.save()

            return redirect("services")

    else:

        form = ServiceForm()

    services = Service.objects.filter(
        business=business
    )

    return render(
        request,
        "dashboard/services.html",
        {
            "form": form,
            "services": services,
        }
    )
@login_required
def edit_service(request, service_id):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    service = get_object_or_404(
        Service,
        id=service_id,
        business=business
    )

    if request.method == "POST":

        form = ServiceForm(
            request.POST,
            instance=service
        )

        if form.is_valid():

            form.save()

            return redirect("services")

    else:

        form = ServiceForm(
            instance=service
        )

    return render(
        request,
        "dashboard/edit_service.html",
        {
            "form": form,
            "service": service,
        }
    )
@login_required
def delete_service(request, service_id):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    service = get_object_or_404(
        Service,
        id=service_id,
        business=business
    )

    service.delete()

    return redirect("services")

@login_required
def edit_working_hour(request, hour_id):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    hour = get_object_or_404(
        WorkingHour,
        id=hour_id,
        business=business
    )

    if request.method == "POST":

        form = WorkingHourForm(
            request.POST,
            instance=hour
        )

        if form.is_valid():

            form.save()

            return redirect("working_hours")

    else:

        form = WorkingHourForm(
            instance=hour
        )

    return render(
        request,
        "dashboard/edit_working_hour.html",
        {
            "form": form,
            "hour": hour,
        }
    )
@login_required
def delete_working_hour(request, hour_id):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    hour = get_object_or_404(
        WorkingHour,
        id=hour_id,
        business=business
    )

    hour.delete()

    return redirect("working_hours")
@login_required
def working_hours(request):

    business = Business.objects.get(owner=request.user)

    if request.method == "POST":

        form = WorkingHourForm(request.POST)

        if form.is_valid():

            working_hour = form.save(commit=False)
            working_hour.business = business
            working_hour.save()

            return redirect("working_hours")

    else:

        form = WorkingHourForm()

    hours = WorkingHour.objects.filter(
        business=business
    )

    return render(
        request,
        "dashboard/working_hours.html",
        {
            "form": form,
            "hours": hours,
        }
    )
@login_required
def customers(request):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    search = request.GET.get("search", "")

    customers = Customer.objects.filter(
        business=business
    )

    if search:

        customers = customers.filter(
            name__icontains=search
        )

    customers = customers.order_by("name")

    total_customers = Customer.objects.filter(
        business=business
    ).count()

    returning_customers = Customer.objects.filter(
    business=business
).count()

    today_customers = Appointment.objects.filter(
        business=business,
        appointment_date=date.today()
    ).values("customer").distinct().count()

    return render(
        request,
        "dashboard/customers.html",
        {
            "customers": customers,
            "search": search,
            "total_customers": total_customers,
            "returning_customers": returning_customers,
            "today_customers": today_customers,
        }
    )
@login_required
def customer_detail(request, customer_id):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    customer = get_object_or_404(
        Customer,
        id=customer_id,
        business=business
    )

    appointments = Appointment.objects.filter(
        customer=customer
    ).order_by(
        "-appointment_date",
        "-appointment_time"
    )

    total_visits = appointments.count()

    total_spent = sum(
        appointment.service.price
        for appointment in appointments
    )

    last_visit = appointments.first()

    return render(
        request,
        "dashboard/customer_detail.html",
        {
            "customer": customer,
            "appointments": appointments,
            "total_visits": total_visits,
            "total_spent": total_spent,
            "last_visit": last_visit,
        }
    )
@login_required
def staff(request):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    staff_members = Staff.objects.filter(
        business=business
    ).order_by("name")

    return render(
        request,
        "dashboard/staff.html",
        {
            "staff_members": staff_members,
        }
    )


@login_required
def add_staff(request):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    if request.method == "POST":

        form = StaffForm(request.POST)

        if form.is_valid():

            staff_member = form.save(
                commit=False
            )

            staff_member.business = business

            staff_member.save()

            return redirect("staff")

    else:

        form = StaffForm()

    return render(
        request,
        "dashboard/add_staff.html",
        {
            "form": form,
        }
    )


@login_required
def edit_staff(request, staff_id):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    staff_member = get_object_or_404(
        Staff,
        id=staff_id,
        business=business
    )

    if request.method == "POST":

        form = StaffForm(
            request.POST,
            instance=staff_member
        )

        if form.is_valid():

            form.save()

            return redirect("staff")

    else:

        form = StaffForm(
            instance=staff_member
        )

    return render(
        request,
        "dashboard/edit_staff.html",
        {
            "form": form,
            "staff_member": staff_member,
        }
    )


@login_required
def delete_staff(request, staff_id):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    staff_member = get_object_or_404(
        Staff,
        id=staff_id,
        business=business
    )

    staff_member.delete()

    return redirect("staff")
