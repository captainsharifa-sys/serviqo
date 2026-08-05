from datetime import datetime, timedelta

from .models import Appointment



def generate_time_slots(
    business,
    service,
    appointment_date
):

    day_name = appointment_date.strftime("%A")


    working_hour = business.working_hours.filter(
        day=day_name
    ).first()


    if not working_hour:
        return []


    if working_hour.is_closed:
        return []


    slots = []


    current_time = datetime.combine(
        appointment_date,
        working_hour.open_time
    )


    end_time = datetime.combine(
        appointment_date,
        working_hour.close_time
    )


    while current_time + timedelta(
        minutes=service.duration
    ) <= end_time:


        slot_time = current_time.time()


        booked = Appointment.objects.filter(
            business=business,
            appointment_date=appointment_date,
            appointment_time=slot_time
        ).exists()


        if not booked:

            slots.append(slot_time.strftime("%H:%M"))


        current_time += timedelta(
            minutes=service.duration
        )


    return slots