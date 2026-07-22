"""
agents/executor.py
-------------------
The Executor Agent takes ONE task (produced by the Planner) and carries it out,
returning a result string.
"""

from models import get_llm
from prompts import EXECUTOR_PROMPT


class ExecutorAgent:
    def __init__(self):
        self.llm = get_llm()
        self.chain = EXECUTOR_PROMPT | self.llm

    def execute(self, task: str, history: str = "") -> str:
        """
        Runs a single task and returns the result text.
        """
        response = self.chain.invoke({"task": task, "history": history})
        return response.content.strip()
