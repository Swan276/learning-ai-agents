specialists = {
    "John": ["Monday", "Tuesday", "Saturday"],
    "May": ["Tuesday", "Sunday"],
    "Jennie": ["Monday", "Wednesday", "Friday"],
    "Paul": ["Wednesday", "Thursday", "Friday"],
    "Jessie": ["Saturday", "Sunday"],
    "Rory": ["Monday", "Tuesday", "Wednesday", "Thursday"],
    "Hailey": ["Thursday", "Saturday", "Sunday"],
}

def get_specialist(name: str = "") -> dict:
    """
    Get specialist and his/her available days. Get all specialists if the name is not given.

    Args:
        name (str): specialist name. Get all specialists if the name is empty.

    Returns:
        dict: A dictionary with the status and specialists' available days.

    Example:
        get_specialists()
        {
            'status': 'success',
            'specialists': [
                "John": ["Monday", "Tuesday", "Saturday"],
                "May": ["Tuesday", "Sunday"],
                "Jennie": ["Monday", "Wednesday", "Friday"]
            ]
        }
        get_specialists(name="John")
        {
            'status': 'success',
            'specialists': [
                {"John": ["Monday", "Tuesday", "Saturday"]}
            ]
        }
    """
    if name == "":
        return {
            "status": "success",
            "specialists": specialists
        }

    specialist = specialists.get(name)
    if specialist:
        return {
            "status": "success",
            "specialists": [specialist]
        }
    else:
        return {
            "status": "failure",
            "message": "Specialist not found."
        }
