from utils.states.customer_info import CustomerInfo
import pandas as pd

def update_appointment_sheet(customer_info: CustomerInfo, booking_id: str = None):
    df = pd.read_csv('./resources/appointments.csv')
    bid = booking_id
    if booking_id:
        df[df['Id'] == booking_id] = customer_info.df_array(booking_id)
    else:
        customer_array = customer_info.df_array()
        df.loc[len(df)] = customer_array
        bid = customer_array[0]
    df.to_csv('./resources/appointments.csv', index=False)
    return bid # id

def book_appointment(customer_info: CustomerInfo, booking_id: str = None) -> dict:
    """
        Book an appointment with the given customer information. Confirm the given information with the customer before using this tool.
        Each service takes an hour, so please check and make sure that the chosen time plus time of the services don't exceed the shop closing time.

        Args:
            customer_info (CustomerInfo): customer information to book an appointment.
            booking_id (str): id of the recently booked appointment if the customer want to update. None if it is a new appointment.

        Returns:
            dict: A dictionary with the status and message.

        Example:
            book_appointment(
                customer_info=CustomerInfo(
                    name="Swan",
                    contact_number="123456789",
                    date_and_time=datetime.datetime(2025, 6, 7),
                    preferred_services=["haircut", "nail"],
                    preferred_specialist="May"
                )
            )
            {
                'status': 'success',
                'message': 'Successfully booked an appointment at {customer_info.date_and_time} for {customer_info.preferred_services}'
                "booking_id": "1234",
            }
    """
    if customer_info.check_if_all_fields_present():
        try:
            booking_id = update_appointment_sheet(customer_info=customer_info, booking_id=booking_id)
            return {
                "status": "success",
                "message": f"Successfully booked an appointment at {customer_info.date_and_time} for {customer_info.preferred_services}{f" with {customer_info.preferred_specialist}" if len(customer_info.preferred_specialist) != 0 else ""}{f"({customer_info.special_requests})" if len(customer_info.special_requests) != 0 else ""}",
                "booking_id": booking_id,
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