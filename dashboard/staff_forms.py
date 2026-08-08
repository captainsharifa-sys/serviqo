from django import forms

from .models import Staff


class StaffForm(forms.ModelForm):

    class Meta:

        model = Staff

        fields = [
            "name",
            "phone",
            "email",
            "job_title",
            "is_active",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Staff member name",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone number",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email address",
                }
            ),

            "job_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Barber, Doctor, Trainer",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }