import asyncio

from dotenv import load_dotenv
import uuid

from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from memory_agent import memory_agent
from utils import call_agent_async

load_dotenv()

# Session
db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

# Session data and Meta
initial_state = {
    "user_name": "Brandon",
    "reminders": []
}
APP_NAME = "Memory Agent"
SESSION_ID = str(uuid.uuid4())
USER_ID = "Brandon"


async def main():
    # Fetch existing session if any
    print("Creating Session")
    existing_session = await session_service.list_sessions(app_name=APP_NAME, user_id=USER_ID)

    if existing_session and len(existing_session.sessions) > 0:
        session_id = existing_session.sessions[0].id
        print(f"Continuing with existing Session Id: {session_id}")
    else:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
            session_id=SESSION_ID
        )
        session_id = session.id
        print("Creating new session")

    # Runner
    runner = Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print("\n Welcome to Memory Chat Agent!")
    print("\n Your reminders will be remembered across sessions")
    print("\n Type 'exit' or 'quit' to end the conversation.")

    while True:
        user_input = input("> ")
        if user_input.lower().strip("> ") in ["exit", "quit"]:
            print("Goodbye!")
            break

        await call_agent_async(runner, USER_ID, session_id, user_input)


if __name__ == "__main__":
    asyncio.run(main())
