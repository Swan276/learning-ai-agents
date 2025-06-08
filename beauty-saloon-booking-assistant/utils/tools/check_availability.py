from datetime import datetime

def check_availability(specialist: str = None, date: datetime = None, time: datetime = None) -> dict:
    """
    Check the availability of specialist, specified date or the time slot.

    Args:
        specialist (str): specialist name.
        date (datetime): date of the appointment.
        time (datetime): time of the appointment.

    Returns:
        dict: A dictionary with the status and message.
    """
    return {
        "status": "available",
    }