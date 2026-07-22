"""
agents/planner.py
------------------
The Planner Agent takes a high-level GOAL and breaks it into an
ordered list of small tasks.
"""

import re
from typing import List

from models import get_llm
from prompts import PLANNER_PROMPT


class PlannerAgent:
    def __init__(self):
        self.llm = get_llm()
        self.chain = PLANNER_PROMPT | self.llm

    def plan(self, goal: str, history: str = "") -> List[str]:
        """
        Returns a list of task strings for the given goal.
        """
        response = self.chain.invoke({"goal": goal, "history": history})
        text = response.content
        return self._parse_tasks(text)

    @staticmethod
    def _parse_tasks(text: str) -> List[str]:
        """
        Turns a numbered-list LLM response into a clean Python list.
        Handles formats like "1. Do X" or "1) Do X".
        """
        tasks = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            cleaned = re.sub(r"^\d+[\.\)]\s*", "", line)
            if cleaned:
                tasks.append(cleaned)
        return tasks
