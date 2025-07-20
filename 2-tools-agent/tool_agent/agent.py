import datetime

from google.adk.agents import Agent

def get_current_time() -> dict:
    """
    Get current time in the format of YYYY-MM-DD HH:MM:SS
    """
    return {
        "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

root_agent = Agent(
    name="tool_agent",
    model="gemini-2.5-flash",
    description="Tool Agent",
    instruction="""
    You are helpful assistant that can use the following tools:
    - get_current_time
    """,
    tools=[get_current_time]
)
