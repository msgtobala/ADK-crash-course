import uuid
import asyncio
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from question_answering_agent import question_answering_agent

load_dotenv()

# state
initial_state = {
    "user_name": "Brandon Hancock",
    "user_preferences": """
        I like to play Pickleball, Disc Golf, and Tennis.
        My favorite food is Mexican.
        My favorite TV show is Game of Thrones.
        Loves it when people like and subscribe to his YouTube channel.
    """,
}

# Session Meta
APP_NAME = "Brandon Bot"
USER_ID = "brandon_hancock"
SESSION_ID = str(uuid.uuid4())


async def main():
    # Session
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )
    print("Created Session successfully")
    print(f"Session Id: {SESSION_ID}")

    # Runner
    runner = Runner(
        app_name=APP_NAME,
        session_service=session_service,
        agent=question_answering_agent,
    )
    print("Created Runner successfully")

    # Create a new message -> Creating a user input event
    new_message = types.Content(
        role="user", parts=[types.Part(text="What is Brandon's favorite TV show?")]
    )

    # Run the runner
    for event in runner.run(session_id=SESSION_ID, user_id=USER_ID, new_message=new_message):
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"Final Response: {event.content.parts[0].text}")

    # Session exploration
    print(f"Session State: {session.state}")

    # Get the session again
    session_value = await session_service.get_session(
        app_name=APP_NAME, session_id=SESSION_ID, user_id=USER_ID
    )

    print(f"Session Value: {session_value.state}")


if __name__ == "__main__":
    asyncio.run(main())
