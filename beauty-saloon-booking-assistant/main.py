from graph import BookingAssistantAgent

agent = BookingAssistantAgent()

def run_booking_assistant():
    for msg in agent.invoke_stream("Hello"):
        print(msg, end="")

    while True:
        print("\n-------------------------")
        user_input = input("Chat (q to quit): ").strip()
        if user_input == "q":
            break
        for msg in agent.invoke_stream(user_input):
            print(msg, end="")

if __name__ == "__main__":
    run_booking_assistant()

