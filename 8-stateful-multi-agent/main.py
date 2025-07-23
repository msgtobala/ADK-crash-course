import asyncio
import uuid

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from dotenv import load_dotenv

from customer_service_agent.agent import customer_service_agent
from utils import add_user_query_to_history, call_agent_async

load_dotenv()

# Session data
initial_state = {
    "user_name": "Brandon Hancock",
    "purchased_courses": [],
    "interaction_history": [],
}
SESSION_ID = str(uuid.uuid4())
USER_ID = "Brandon"
APP_NAME = "Customer Support"


async def main():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        session_id=SESSION_ID,
        user_id=USER_ID,
        state=initial_state,
    )

    runner = Runner(
        app_name=APP_NAME,
        session_service=session_service,
        agent=customer_service_agent
    )

    # ===== PART 5: Interactive Conversation Loop =====
    print("\nWelcome to Customer Service Chat!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input = input("> ")
        if user_input.strip("> ") in ["exit", "quit"]:
            print("Goodbye!")
            break
        await add_user_query_to_history(
            session_service, APP_NAME, USER_ID, SESSION_ID, user_input
        )
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

    final_session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print("\nFinal Session State:")
    for key, value in final_session.state.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
