import pandas as pd
from pandas import Series

def convert_to_dict(row: Series, results_dict: dict) -> dict:
    name = row["Name"]
    days = []
    for series_name, series in row.items():
        if series == 1:
            days.append(series_name)
    results_dict[name] = days
    return results_dict


def get_specialist(name: str = None, day: str = None) -> dict:
    """
    Get specialist and his/her available days or get all specialists of the given day. Get all specialists if the name is not given.

    Args:
        name (str): specialist name. Get all specialists if the name is not given.
        day (str): day of the week. (e.g. Monday, Sunday)

    Returns:
        dict: A dictionary with the status and specialists' available days.

    Example:
        get_specialists()
        {
            'status': 'success',
            'specialists': {
                "John": ["Monday", "Tuesday", "Saturday"],
                "May": ["Tuesday", "Sunday"],
                "Jennie": ["Monday", "Wednesday", "Friday"]
            }
        }
        get_specialists(name="John")
        {
            'status': 'success',
            'specialists': {
                "John": ["Monday", "Tuesday", "Saturday"]
            }
        }
    """
    df = pd.read_csv('./resources/work_shifts.csv')
    day_mask = df[day] == 1 if day else None
    name_mask = df["Name"] == name if name else None

    results = None
    if (day_mask is not None) and (name_mask is not None):
        results = df[day_mask & name_mask]
    elif day_mask is not None:
        results = df[day_mask]
    elif name_mask is not None:
        results = df[name_mask]
    else:
        results = df

    if len(results) == 0:
        return {
            "status": "failure",
            "message": "Specialist not found."
        }

    results_dict = {}
    results.apply(lambda row: convert_to_dict(row, results_dict), axis=1)

    return {
        "status": "success",
        "specialists": results_dict
    }
