from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = [
            "service",
            "customer_name",
            "customer_phone",
            "customer_email",
            "appointment_date",
            "appointment_time",
        ]

        widgets = {
            "appointment_date": forms.DateInput(
                attrs={"type": "date"}
            ),

            "appointment_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
        }

    def __init__(self, *args, **kwargs):
        business = kwargs.pop("business", None)

        super().__init__(*args, **kwargs)

        if business:
            self.fields["service"].queryset = business.services.all()
        else:
            self.fields["service"].queryset = self.fields["service"].queryset.none()