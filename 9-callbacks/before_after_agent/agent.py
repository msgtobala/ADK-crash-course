import uuid
from datetime import datetime
from typing import Optional

from google.adk.agents import Agent
from google.genai import types
from google.adk.agents.callback_context import CallbackContext


def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
        Simple callback that logs when the agent starts processing a request.

        Args:
            callback_context: Contains state and context information

        Returns:
            None to continue with normal agent processing
    """
    # Extract state
    state = callback_context.state

    # record datatime
    timestamp = datetime.now()

    # check agent name
    if "agent_name" not in state:
        state["agent_name"] = "SimpleChatBot"

    if "reqeust_counter" not in state:
        state["reqeust_counter"] = 1
    else:
        state["reqeust_counter"] += 1

    state["request_start_time"] = timestamp

    print("Before Agent Callback")
    return None


def after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
        Simple callback that logs when the agent finishes processing a request.

        Args:
            callback_context: Contains state and context information

        Returns:
            None to continue with normal agent processing
        """

    # Extract the state
    state = callback_context.state

    timestamp = datetime.now()
    state["request_end_time"] = timestamp
    state["duration"] = timestamp - state["request_start_time"]

    print("After Agent Callback")
    return None


root_agent = Agent(
    name="before_after_agent",
    model="gemini-2.5-flash",
    description="A basic agent that demonstrates before and after agent callbacks",
    instruction="""
        You are a friendly greeting agent. Your name is {agent_name}.

        Your job is to:
        - Greet users politely
        - Respond to basic questions
        - Keep your responses friendly and concise
        """,
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
)
