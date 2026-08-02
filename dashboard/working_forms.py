from django import forms
from .models import WorkingHour


class WorkingHourForm(forms.ModelForm):

    class Meta:
        model = WorkingHour
        fields = [
            "day",
            "open_time",
            "close_time",
            "is_closed",
        ]