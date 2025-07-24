"""
Sequential Agent with a Minimal Callback

This example demonstrates a lead qualification pipeline with a minimal
before_agent_callback that only initializes state once at the beginning.
"""

from google.adk.agents import SequentialAgent

from .sub_agents.recommender import action_recommender_agent
from .sub_agents.scorer import lead_scorer_agent

# Import the sub_agents
from .sub_agents.validator import lead_validator_agent

# Create the sequential agent with minimal callback
root_agent = SequentialAgent(
    name="LeadQualificationPipeline",
    sub_agents=[lead_validator_agent, lead_scorer_agent, action_recommender_agent],
    description="A pipeline that validates, scores, and recommends actions for sales leads",
)
