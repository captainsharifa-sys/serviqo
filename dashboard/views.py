from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import BusinessForm
from .models import Business


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
        {"form": form}
    )