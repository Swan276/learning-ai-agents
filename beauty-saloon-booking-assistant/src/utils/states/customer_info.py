from datetime import datetime

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
    )
    special_requests: str = Field(
        description="Special requests for the appointment",
    )
    @property
    def customer_information(self) -> str:
        return f"Name: {self.name}\nContact Number: {self.contact_number}\nPreferred Services: {self.preferred_services}\nDate and Time: {self.date_and_time}\nPreferred Specialist: {self.preferred_specialist}\nSpecial Requests: {self.special_requests}"