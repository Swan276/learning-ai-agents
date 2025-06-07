from datetime import datetime

from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, Field

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
        default="None"
    )
    special_requests: str = Field(
        description="Special requests for the appointment",
        default="None"
    )
    @property
    def customer_information(self) -> str:
        return f"Name: {self.name}\nContact Number: {self.contact_number}\nPreferred Services: {self.preferred_services}\nDate and Time: {self.date_and_time}\nPreferred Specialist: {self.preferred_specialist}\nSpecial Requests: {self.special_requests}"

def get_services() -> list[str]:
    """Gets all the available services."""
    return ["haircut", "hairstyling", "hair treatment"]

def get_specialists() -> dict[str, list[str]]:
    """Gets all the available hair specialists with their available days"""
    return {
        "John": ["Monday", "Wednesday", "Friday"],
        "May": ["Tuesday", "Wednesday", "Thursday"],
        "Jessie": ["Monday", "Tuesday", "Friday"],
        "Jane": ["Saturday", "Sunday"],
        "Jack": ["Saturday", "Sunday"],
    }

def get_current_datetime() -> datetime:
    """Get current datetime"""
    return datetime.now()

def get_booking_policy_and_guideline() -> str:
    """Get booking policy and guideline to follow
    Call this before making any booking appointment and validate customer request using this"""
    return """
    1. Shop Information
Salon Information to Provide (if asked or when appropriate):
● Name: The White Swan
● Location: Dublin 2, O’Connell Street, in the city centre
● Contact Number: 087 123 4567
● Operating Hours: Everyday from 10am-7pm
● Social Media/Website: thewhiteswan.com
2. Gathering Booking Details
Use the following checklist to collect all necessary information for a booking:
Booking Information Checklist:
● Full Name: "May I have your full name, please?"
● Contact Number: "Could you provide a phone number we can reach you at?"
● Preferred Service(s): "Which service(s) would you like to book?"
● Preferred Date & Time: "Do you have a preferred date and time in mind?"
● Preferred Specialist (if any): "Would you like to request a specific specialist or stylist?"
● Special Requests (if any): "Do you have any specific requests, such as allergies, privacy preferences, or special needs?"
Confirm all details at the end of this section. "Just to confirm, you’re booking [Service] on [Date] at [Time] with [Specialist, if selected]. Is that correct?"
3. Booking Policy
Kindly explain the booking policies after gathering details:
Booking Policy:
● Advance Booking: Appointments can be made up to 3 days in advance.
● Minimum Notice: No minimum time required – same-day bookings are welcome if slots are available.
● Walk-ins: Walk-ins are welcome and will be accommodated based on availability.
● Changes & Cancellations: Please notify us at least 4 hours in advance for any changes or cancellations.
● Late Arrivals: A 10-minute grace period is allowed. Beyond this, we may need to reschedule depending on availability.
“Would you like to proceed with confirming your appointment now?”
    """

def make_booking_appointment(customer_info: CustomerInfo) -> dict[str, str]:
    """Make a booking appointment using customer information
    Validate the fields using the followings:
    - date_and_time (with get_booking_policy_and_guideline and chosen specialist on the date_and_time using get_specialists)
    - preferred_specialist (with get_specialists)
    - special_requests (with get_booking_policy_and_guideline)"""
    if customer_info.date_and_time.weekday() == 2:
        return {
            "status": "Failed",
            "error_message": "Unable to book appointment. Wednesday is not available",
        }
    else:
        return {
            "status": "Success",
        }

tools = [get_services]

model = ChatOllama(
    model="granite3.3:8b",
    temperature=0
).bind_tools(tools)

system_assistant_prompt = SystemMessage(
    content="""
    Your name is Hanna. You are a helpful booking assistant for the White Swan beauty saloon.
    Greet customer with the line "Thank you for contacting The White Swan Saloon! I'm Hanna, your booking assistant. How can I help you with your beauty needs today?".
    Use the tools available to assist the customer.
    """
)

def assistant(state: MessagesState):
    return {"messages": [model.invoke([system_assistant_prompt] + state["messages"])]}

builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

graph = builder.compile()
