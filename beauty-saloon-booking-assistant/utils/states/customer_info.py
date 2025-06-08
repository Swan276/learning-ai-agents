import uuid
from datetime import datetime, timedelta
from typing import Self
from pydantic import Field, BaseModel

class CustomerInfo(BaseModel):
    name: str = Field(
        description="Full name of the customer",
    )
    contact_number: str = Field(
        description="Contact number of the customer",
    )
    preferred_services: list[str] = Field(
        description="Services that the customer prefers for the appointment",
    )
    date_and_time: datetime = Field(
        description="Date and time of the appointment",
    )
    preferred_specialist: str = Field(
        description="Preferred specialist for the appointment",
        default=""
    )
    special_requests: str = Field(
        description="Special requests for the appointment",
        default=""
    )
    @property
    def customer_information(self) -> str:
        return f"Name: {self.name}\nContact Number: {self.contact_number}\nPreferred Services: {self.preferred_services}\nDate and Time: {self.date_and_time}\nPreferred Specialist: {self.preferred_specialist}\nSpecial Requests: {self.special_requests}"

    def df_array(self, booking_id: str = None):
        booking_id = booking_id if booking_id is not None else str(uuid.uuid4())
        start_datetime = self.date_and_time
        end_datetime = self.date_and_time + timedelta(hours=len(self.preferred_services))
        return [booking_id, self.name, self.contact_number, ','.join(self.preferred_services),
                self.date_and_time.strftime("%Y-%m-%d"), start_datetime.strftime("%H:%M"), end_datetime.strftime("%H:%M"),
                self.preferred_specialist, self.special_requests]

    def check_if_all_fields_present(self) -> bool:
        if self.name and self.contact_number and self.preferred_services and self.date_and_time:
            return True
        else:
            return False

    def __str__(self):
        return self.customer_information