from datetime import datetime, time

import pandas as pd

opening_time = time(hour=10)
closing_time = time(hour=19)

def get_available_timeslots(date: datetime) -> dict:
    """
    Get the available time slots on the specified date.

    Args:
        date (datetime): date to check the available time slots.

    Returns:
        dict: A dictionary with the status and a list of time slots.
    """

    try:
        df = pd.read_csv('./resources/appointments.csv')
        # TODO: check availability conditioning with specialists. make sure no overlaps.
        # TODO: check availability conditioning with specified time.

        df = df.sort_values('Start Time').reset_index(drop=True)
        date_appointments = df[df["Date"] == date.strftime("%Y-%m-%d")].reset_index(drop=True)

        if len(date_appointments) == 0:
            return {
                "status": "available",
                "timeslots": [
                    "10:00-19:00"
                ],
            }

        timeslots = []
        first_appointment_start = datetime.strptime(
            date_appointments.loc[0, 'Start Time'],
            "%H:%M"
        ).time()
        if first_appointment_start > opening_time:
            timeslots.append(f'{opening_time.strftime("%H:%M")}-{first_appointment_start.strftime("%H:%M")}')

        for i in range(len(date_appointments) - 1):
            end_current = date_appointments.loc[i, 'End Time']
            start_next = date_appointments.loc[i + 1, 'Start Time']

            if start_next > end_current:
                timeslots.append(f'{end_current}-{start_next}')

        last_appointment_end = datetime.strptime(
            date_appointments.loc[len(date_appointments) - 1, 'End Time'],
            "%H:%M"
        ).time()
        if last_appointment_end < closing_time:
            timeslots.append(f'{last_appointment_end.strftime("%H:%M")}-{closing_time.strftime("%H:%M")}')

        if len(timeslots) == 0:
            return {
                "status": "not available",
                "timeslots": []
            }

        return {
            "status": "available",
            "timeslots": timeslots,
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": str(e),
            "timeslots": [],
        }