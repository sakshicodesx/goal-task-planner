"""
engine/guard.py
----------------
ScopeGuard runs BEFORE the PlannerAgent. It checks whether the user's
message is actually something this agent should handle (see
config.BOT_SCOPE_DESCRIPTION), or whether it's an unrelated / off-topic
question, small talk, or an attempt to get the agent to act outside its
defined purpose.

Kept as a single, cheap LLM call so it's easy to reason about and easy
to swap for a keyword-based check if you want zero extra API calls.
"""

from models import get_llm
from prompts import GUARD_PROMPT
from config import OFF_TOPIC_MESSAGE


class ScopeGuard:
    def __init__(self):
        self.llm = get_llm()
        self.chain = GUARD_PROMPT | self.llm

    def is_on_topic(self, message: str) -> bool:
        """
        Returns True if the message fits the agent's defined scope,
        False otherwise. Fails "open" is NOT used here on purpose --
        if the classifier response is unclear, we treat it as off-topic
        so the agent stays safely inside its lane.
        """
        response = self.chain.invoke({"message": message})
        verdict = response.content.strip().upper()
        return verdict.startswith("ON_TOPIC")

    @staticmethod
    def refusal_message() -> str:
        return OFF_TOPIC_MESSAGE
