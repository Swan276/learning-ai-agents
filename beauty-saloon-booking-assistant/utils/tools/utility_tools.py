from datetime import datetime

def get_today_date_and_time() -> dict:
    """
    Get today date and time to help user with booking. Parse phrases such as today, tomorrow, etc. into datetime using this tool.

    Returns:
        dict: A dictionary with the status and current datetime.

    Example:
        get_current_date_and_time()
        {'status': 'success', 'current_datetime': datetime.datetime(2025, 6, 7, 12, 22, 56, 727686)}
    """
    return {
        'status': "success",
        'current_datetime': datetime.now()
    }