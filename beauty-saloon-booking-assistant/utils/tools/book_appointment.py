from utils.states.customer_info import CustomerInfo

def book_appointment(customer_info: CustomerInfo) -> dict:
    """
        Book an appointment with the given customer information. Confirm the given information with the customer before using this tool.

        Args:
            customer_info (CustomerInfo): customer information to book an appointment.

        Returns:
            dict: A dictionary with the status and message.

        Example:
            book_appointment(
                customer_info=CustomerInfo(
                    name="Swan",
                    contact_number="123456789",
                    date_and_time=datetime.datetime(2025, 6, 7)
                    preferred_services=["haircut", "nail"],
                    preferred_specialist="May"
                )
            )
            {
                'status': 'success',
                'message': 'Successfully booked an appointment at {customer_info.date_and_time} for {customer_info.preferred_services}'
            }
    """
    if customer_info.check_if_all_fields_present():
        try:
            with open("./resources/appointments.csv", "a") as f:
                f.write(f"\n{customer_info.csv}")
            return {
                "status": "success",
                "message": f"Successfully booked an appointment at {customer_info.date_and_time} for {customer_info.preferred_services}{f" with {customer_info.preferred_specialist}" if len(customer_info.preferred_specialist) != 0 else ""}{f"({customer_info.special_requests})" if len(customer_info.special_requests) != 0 else ""}"
            }
        except Exception as e:
            return {
                "status": "failure",
                "message": f"Error booking appointment: f{str(e)}"
            }
    else:
        return {
            "status": "failure",
            "message": "Error booking appointment: Please confirm all the customer information is present"
        }