from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import BusinessForm


@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")


@login_required
def create_business(request):

    if request.method == "POST":
        form = BusinessForm(request.POST)

        if form.is_valid():
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