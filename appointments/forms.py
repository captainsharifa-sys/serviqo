from django import forms

from .models import Appointment
from dashboard.models import WorkingHour


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

        self.business = kwargs.pop(
            "business",
            None
        )

        super().__init__(*args, **kwargs)


        if self.business:

            self.fields["service"].queryset = (
                self.business.services.all()
            )

        else:

            self.fields["service"].queryset = (
                self.fields["service"].queryset.none()
            )


    def clean(self):

        cleaned_data = super().clean()

        service = cleaned_data.get("service")
        appointment_date = cleaned_data.get("appointment_date")
        appointment_time = cleaned_data.get("appointment_time")


        if (
            self.business
            and service
            and appointment_date
            and appointment_time
        ):

            # Check working hours

            day_name = appointment_date.strftime("%A")


            working_hour = WorkingHour.objects.filter(
                business=self.business,
                day=day_name
            ).first()


            if not working_hour:

                raise forms.ValidationError(
                    "This business has no working hours set for this day."
                )


            if working_hour.is_closed:

                raise forms.ValidationError(
                    f"This business is closed on {day_name}."
                )


            if (
                appointment_time < working_hour.open_time
                or appointment_time > working_hour.close_time
            ):

                raise forms.ValidationError(
                    f"Business hours are "
                    f"{working_hour.open_time.strftime('%H:%M')} "
                    f"to "
                    f"{working_hour.close_time.strftime('%H:%M')}."
                )


            # Check duplicate bookings

            exists = Appointment.objects.filter(
                business=self.business,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
            ).exists()


            if exists:

                raise forms.ValidationError(
                    "This time slot is already booked."
                )


        return cleaned_data