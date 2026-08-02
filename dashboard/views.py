from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import BusinessForm
from .service_forms import ServiceForm
from .working_forms import WorkingHourForm

from .models import Business, Service, WorkingHour

@login_required
def dashboard(request):

    business = Business.objects.filter(owner=request.user).first()

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "business": business
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

    services = Service.objects.filter(business=business)

    return render(
        request,
        "dashboard/services.html",
        {
            "form": form,
            "services": services,
        }
    )
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
    
        